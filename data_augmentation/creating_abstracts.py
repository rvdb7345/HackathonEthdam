from torchtext.models import T5_BASE_GENERATION
from functools import partial
from torch.utils.data import DataLoader
from torchtext.datasets import CNNDM
from torchtext.prototype.generate import GenerationUtils


def create_summary(text):
    # Load the T5 model and its components
    transform = T5_BASE_GENERATION.transform()
    model = T5_BASE_GENERATION.get_model()
    model.eval()

    # Set up the sequence generator
    sequence_generator = GenerationUtils(model)

    # Configuration
    beam_size = 1
    eos_idx = 1

    # Define the input text for summarization
    input_text = ["summarize: " + text]

    # Encode the input text using the model's tokenizer
    model_input = transform(input_text)

    # Generate the summary using the sequence generator
    model_output = sequence_generator.generate(
        model_input, eos_idx=eos_idx, num_beams=beam_size
    )
    output_text = transform.decode(model_output.tolist())

    # Print the generated summary
    return output_text[0]


create_summary(
    "At its core, Ethereum is a decentralized global software platform powered by blockchain technology. It is most commonly known for its native cryptocurrency, ether (ETH). Ethereum can be used by anyone to create any secured digital technology. It has a token designed to pay for work done supporting the blockchain, but participants can also use it to pay for tangible goods and services if accepted. Ethereum is designed to be scalable, programmable, secure, and decentralized. It is the blockchain of choice for developers and enterprises creating technology based upon it to change how many industries operate and how we go about our daily lives. It natively supports smart contracts, an essential tool behind decentralized applications. Many decentralized finance (DeFi) and other applications use smart contracts in conjunction with blockchain technology."
)
