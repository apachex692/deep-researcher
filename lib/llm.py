from abc import ABC, abstractmethod
from typing import Optional

from google.genai import Client
from google.genai.types import GenerateContentResponseUsageMetadata
from openai import OpenAI
from openai.types import CompletionUsage
from pydantic import BaseModel

from lib.constants import LLMIdentifier
from lib.log import logger
from lib.types import ModelProvider


class LLMModel(ABC):
    def __init__(
        self, llm_identifier: LLMIdentifier, llm_instance: OpenAI | Client
    ):
        if (
            isinstance(llm_instance, OpenAI)
            and llm_identifier.value.model_provider != ModelProvider.OPENAI
        ) or (
            isinstance(llm_instance, Client)
            and llm_identifier.value.model_provider != ModelProvider.GOOGLE
        ):
            raise ValueError("Mismatch: LLM Model Provider and LLM Instance")

        self.llm_identifier = llm_identifier
        self.llm_instance = llm_instance

    @abstractmethod
    def generate_llm_response(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[BaseModel] = None,
    ) -> tuple[
        BaseModel | str, CompletionUsage | GenerateContentResponseUsageMetadata
    ]: ...


class OpenAICompatibleLLMModel(LLMModel):
    def __init__(self, llm_identifier: LLMIdentifier, llm_instance: OpenAI):
        super().__init__(
            llm_identifier=llm_identifier, llm_instance=llm_instance
        )

    def generate_llm_response(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[BaseModel] = None,
    ) -> tuple[BaseModel | str, CompletionUsage]:
        logger.info(
            "Generating LLM Response: %s",
            "structured_completion" if response_format else "completion",
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        try:
            if response_format:
                response = self.llm_instance.beta.chat.completions.parse(
                    model=self.llm_identifier.value.model_identifier,
                    messages=messages,
                    response_format=response_format,
                    timeout=120000,
                )
                result = response.choices[0].message.parsed

            else:
                response = self.llm_instance.chat.completions.create(
                    model=self.llm_identifier.value.model_identifier,
                    messages=messages,
                )
                result = response.choices[0].message.content
        except TimeoutError:
            logger.error(
                "OpenAI: Request Timeout for Query: %s",
                user_prompt,
            )
            logger.warning("Returning Empty Response")
            return "", CompletionUsage(
                completion_tokens=0, prompt_tokens=0, total_tokens=0
            )

        return result, response.usage


class GeminiLLMModel(LLMModel):
    def __init__(self, llm_identifier: LLMIdentifier, llm_instance: Client):
        super().__init__(
            llm_identifier=llm_identifier, llm_instance=llm_instance
        )

    def generate_llm_response(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[BaseModel] = None,
    ) -> tuple[BaseModel | str, GenerateContentResponseUsageMetadata]:
        logger.info(
            "Generating LLM Response: %s",
            "structured_completion" if response_format else "completion",
        )

        if response_format:
            response = self.llm_instance.models.generate_content(
                model=self.llm_identifier.value.model_identifier,
                contents=user_prompt,
                config={
                    "response_mime_type": "application/json",
                    "system_instruction": system_prompt,
                    "response_schema": response_format,
                },
            )
            result = response.parsed

        else:
            response = self.llm_identifier.models.generate_content(
                model=self.llm_identifier.value.model_identifier,
                config={
                    "system_instruction": system_prompt,
                },
                contents=[user_prompt],
            )
            result = response.text

        return result, response.usage
