from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel



#  BIAS DETECTION PROMPT & CHAIN

bias_detection_prompt = """
You are an AI language model that detects bias in user given input and data and categories bias type in user input data. If no bias is found in user input so simply said no bias detected.
you do not write correct statement which is bias free.
{input_text}
"""

def get_bias_detector_chain(llm: BaseLanguageModel = None) -> LLMChain:
    llm = llm or ChatOpenAI(temperature=0.3)
    prompt = PromptTemplate(
        input_variables=["input_text"],
        template=bias_detection_prompt
    )
    return LLMChain(llm=llm, prompt=prompt)

def detect_bias(input_text: str) -> str:
    chain = get_bias_detector_chain()
    response = chain.run({"input_text": input_text})
    return response



#  BIAS SCORING PROMPT & CHAIN

bias_score_prompt = """
You are a bias detection system. Analyze the following text and give a bias score from 0 to 100.

Scoring Guide:
- 0–10: Neutral
- 11–40: Slightly biased
- 41–70: Clearly biased
- 71–100: Strongly biased, problematic

Text:
{input_text}

Respond only with a number.
"""

def get_bias_score_chain() -> LLMChain:
    llm = ChatOpenAI(temperature=0.2)
    prompt = PromptTemplate(
        input_variables=["input_text"],
        template=bias_score_prompt
    )
    return LLMChain(llm=llm, prompt=prompt)

def compute_bias_score(input_text: str) -> int:
    chain = get_bias_score_chain()
    response = chain.run({"input_text": input_text})
    try:
        return int(response.strip())
    except ValueError:
        return -1  



# SUGGESTION GENERATOR PROMPT & CHAIN

rewrite_suggestions_prompt = """
Rewrite the  text to remove bias while keeping the meaning the same. Only return the rewritten text
Biased Sentences:
{biased_sentences}

Return the improved, unbiased versions clearly.
"""

def get_suggestion_chain() -> LLMChain:
    llm = ChatOpenAI(temperature=0.3)
    prompt = PromptTemplate(
        input_variables=["biased_sentences"],
        template=rewrite_suggestions_prompt
    )
    return LLMChain(llm=llm, prompt=prompt)

def generate_rewrite_suggestions(biased_sentences: list[str]) -> str:
    if not biased_sentences:
        return "✅ No biased sentences found. No rewriting needed."

    input_text = "\n".join(biased_sentences)
    chain = get_suggestion_chain()
    response = chain.run({"biased_sentences": input_text})
    return response



# FACT-BASED GENERAL CHAT Bot

chat_about_bias_prompt = """
You are a fact-checking AI assistant. Your job is to provide strictly accurate, neutral, and verifiable responses.
If the user's input contains false or misleading information, politely correct it and provide the factual version. Do not speculate or hallucinate. If you're unsure, say so. Support all claims with facts.if a user give you correct information so simply relpy Information is correct .

User input:
{user_input}
"""

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate



def get_fact_chain() -> LLMChain:
    llm = ChatOpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=chat_about_bias_prompt.strip()
    )
    return LLMChain(llm=llm, prompt=prompt)

def fact(input_text: str) -> str:
    chain = get_fact_chain()
    return chain.run({"user_input": input_text})
