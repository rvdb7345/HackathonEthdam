import pickle

import pandas as pd
from data_selection.topic_modelling import get_topics_out

# from data_selection.data_selection import select_representative_documents
from data_augmentation.classifying_data import grouping_news_article_per_week
from sklearn.metrics.pairwise import cosine_similarity
import torch.utils.data as data_utils

import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import umap
import matplotlib.pyplot as plt
from transformers import AdamW, BertModel, RobertaModel
import torch
from torch.utils.data import DataLoader, Dataset, TensorDataset
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, losses

# from transformers import BertConfig, BertModel, AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')

from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
model_name = "yiyanghkust/finbert-pretrain"
# BertForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
# model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3).base_model
model = BertModel.from_pretrained(model_name)

# pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding = 'max_length')


def preprocessing_for_bert(data):
    """Perform required preprocessing steps for pretrained BERT.
    @param    data (np.array): Array of texts to be processed.
    @return   input_ids (torch.Tensor): Tensor of token ids to be fed to a model.
    @return   attention_masks (torch.Tensor): Tensor of indices specifying which
                  tokens should be attended to by the model.
    """
    # create empty lists to store outputs
    input_ids = []
    attention_masks = []

    # for every sentence...

    for sent in tqdm(data):
        # 'encode_plus will':
        # (1) Tokenize the sentence
        # (2) Add the `[CLS]` and `[SEP]` token to the start and end
        # (3) Truncate/Pad sentence to max length
        # (4) Map tokens to their IDs
        # (5) Create attention mask
        # (6) Return a dictionary of outputs
        encoded_sent = tokenizer.encode_plus(
            text=sent,  # preprocess sentence
            add_special_tokens=True,  # Add `[CLS]` and `[SEP]`
            max_length=512,  # Max length to truncate/pad
            pad_to_max_length=True,  # pad sentence to max length
            return_attention_mask=True  # Return attention mask
        )
        # Add the outputs to the lists
        input_ids.append(encoded_sent.get('input_ids'))
        attention_masks.append(encoded_sent.get('attention_mask'))

    # convert lists to tensors
    input_ids = torch.tensor(input_ids)
    attention_masks = torch.tensor(attention_masks)

    return input_ids, attention_masks

def fine_tune_language_model(model, df):
    # Set the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda" and torch.cuda.is_mps_available():
        torch.cuda.set_device(torch.cuda.current_device())

    # Print device information
    print(f"Device: {device}")

    # Set the loss function
    loss_function = losses.CosineSimilarityLoss(model)
    input_features = df['content'].tolist()
    labels = df['keywords'].tolist()

    tokenised_inputs, att_inputs = preprocessing_for_bert(input_features)
    label_inputs, att_labels = preprocessing_for_bert(labels)

    # input_features = model({'input_ids': tokenised_inputs, 'attention_mask': att_inputs})
    # labels = model({'input_ids': label_inputs, 'attention_mask': att_labels})
    train_data = TensorDataset(tokenised_inputs, att_inputs, label_inputs, att_labels)
    train_dataloader = DataLoader(train_data, batch_size=16)

    # Set the optimizer
    optimizer = AdamW(model.parameters(), lr=2e-5)

    # Fine-tune the language model
    model.to(device)
    model.train()

    # tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

    num_epochs = 3
    for epoch in range(num_epochs):
        running_loss = 0.0
        for doc_inputs, doc_att, label_inputs, label_att in tqdm(train_dataloader, desc=f"Epoch {epoch + 1}/{num_epochs}"):
            optimizer.zero_grad()
            document_embeddings = model(doc_inputs, doc_att).last_hidden_state[:, 0, :]
            keyword_embeddings = model(label_inputs, label_att).last_hidden_state[:, 0, :]
            distances = cosine_similarity(doc_embedding, candidate_embeddings)

            loss = loss_function(document_embeddings, keyword_embeddings)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        epoch_loss = running_loss / len(train_dataloader)
        print(f"Epoch {epoch + 1} Loss: {epoch_loss}")

    # Return the fine-tuned model
    return model


def deprecated_select_representative_documents(df, num_clusters=3, num_representatives=1):
    # Load pre-trained language model for text embedding
    # configuration = BertConfig()
    #
    # # Initializing a model (with random weights) from the bert-base-uncased style configuration
    # model = BertModel(configuration)
    #
    # # Fine-tune the language model on keywords
    # fine_tune_language_model(model, df)

    # Embed the documents
    tokenized_text, att = preprocessing_for_bert(df['content'].tolist())

    batch_size = 16
    train_data = data_utils.TensorDataset(tokenized_text,
                                          att)
    train_loader = data_utils.DataLoader(train_data, batch_size, drop_last=False, shuffle=True)

    document_embeddings = np.zeros((len(df['content'].tolist()), 768))
    batch = 0
    for idx, (tok_text, at) in tqdm(enumerate(train_loader)):
        document_embedding = model(tok_text, at)[0][:, 1:-1, :].detach().numpy().mean(axis=1)
        document_embeddings[idx*batch_size:idx*batch_size + len(document_embedding), :] = document_embedding
        batch += 1

    document_embeddings = (document_embeddings - document_embeddings.mean()) / document_embeddings.std()

    np.save('embeddings.npy', document_embeddings)

    # Perform dimensionality reduction using UMAP
    clusterable_embedding = umap.UMAP(
        n_neighbors=30,
        min_dist=0.0,
        n_components=2,
        random_state=42,
        metric='cosine'
    )
    reduced_embeddings = clusterable_embedding.fit_transform(document_embeddings)

    # Cluster the reduced embeddings
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(reduced_embeddings)

    # Select representative documents from each cluster
    selected_documents = []
    for cluster_id in range(num_clusters):
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        cluster_embeddings = document_embeddings[cluster_indices]

        # Find the indices of the representative documents
        representative_indices = np.argpartition(
            np.linalg.norm(cluster_embeddings - np.mean(cluster_embeddings, axis=0), axis=1),
            num_representatives
        )[:num_representatives]

        # Append the representative documents to the selected documents list
        selected_documents.extend([df['content'].iloc[cluster_indices[idx]] for idx in representative_indices])

    # Plot the UMAP visualization
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=cluster_labels, cmap='viridis')
    plt.title('UMAP Visualization of Document Embeddings')
    plt.show()

    return selected_documents


def select_representative_documents(news_last_week, num_articles_to_publish, plot_clusters=False):
    print(f'We have {len(news_last_week)} from last week.')

    # Example usage
    news_last_week.dropna(subset=['content', 'keywords'], inplace=True)

    # representative_documents = select_representative_documents(news_last_week, num_clusters=5, num_representatives=1)
    # for doc in representative_documents:
    #     print(doc)

    representative_docs = get_topics_out((news_last_week['title']).tolist(), plot=plot_clusters)

    articles_to_publish = pd.DataFrame()
    for subject_idx, representative_articles in representative_docs.items():
        if not subject_idx == -1 and not subject_idx > num_articles_to_publish + 1:
            article_to_publish = news_last_week.loc[news_last_week['title'] == representative_articles[0], :]
            articles_to_publish = pd.concat([articles_to_publish, article_to_publish])

    return articles_to_publish

if __name__ == '__main__':
    formatted_news = pd.read_csv('data/20230520_combined.csv', engine='python')
    news_last_week = grouping_news_article_per_week(formatted_news)

    articles_to_publish = select_representative_documents(news_last_week,
                                                          num_articles_to_publish=10,
                                                          plot_clusters=False)
    print(articles_to_publish)

