from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def code_llama(model_path='./models/codellama-7b-instruct-q4_0.gguf'):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(model_path=model_path,
                   n_ctx=2048,
                   max_tokens=200,
                   n_gpu_layers=2,
                   callback_manager=callback_manager,
                   use_mlock=True)
    return llm
