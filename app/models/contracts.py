from pydantic import BaseModel, ConfigDict, Field


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class SmsRequest(ContractModel):
    from_: str = Field(alias="from")
    to: str
    body: str | None = None
    message_sid: str
    trace_id: str


class VoiceRequest(ContractModel):
    from_: str = Field(alias="from")
    to: str
    call_sid: str
    trace_id: str
    public_base_url: str | None = None


class ErrorPayload(BaseModel):
    code: str
    message: str
    trace_id: str | None = None
    retryable: bool = False
    details: dict = Field(default_factory=dict)


class ErrorEnvelope(BaseModel):
    error: ErrorPayload
