from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PollutionResults(_message.Message):
    __slots__ = ["avg", "desv", "time"]
    AVG_FIELD_NUMBER: _ClassVar[int]
    DESV_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    avg: float
    desv: float
    time: float
    def __init__(self, time: _Optional[float] = ..., avg: _Optional[float] = ..., desv: _Optional[float] = ...) -> None: ...

class RawMeteoData(_message.Message):
    __slots__ = ["humidity", "id", "temperature", "timestamp"]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    humidity: float
    id: str
    temperature: float
    timestamp: int
    def __init__(self, id: _Optional[str] = ..., temperature: _Optional[float] = ..., humidity: _Optional[float] = ..., timestamp: _Optional[int] = ...) -> None: ...

class RawPollutionData(_message.Message):
    __slots__ = ["co2", "id", "timestamp"]
    CO2_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    co2: float
    id: str
    timestamp: int
    def __init__(self, id: _Optional[str] = ..., co2: _Optional[float] = ..., timestamp: _Optional[int] = ...) -> None: ...

class Results(_message.Message):
    __slots__ = ["pollution_results", "wellness_results"]
    POLLUTION_RESULTS_FIELD_NUMBER: _ClassVar[int]
    WELLNESS_RESULTS_FIELD_NUMBER: _ClassVar[int]
    pollution_results: PollutionResults
    wellness_results: WellnessResults
    def __init__(self, wellness_results: _Optional[_Union[WellnessResults, _Mapping]] = ..., pollution_results: _Optional[_Union[PollutionResults, _Mapping]] = ...) -> None: ...

class WellnessResults(_message.Message):
    __slots__ = ["avg", "desv", "time"]
    AVG_FIELD_NUMBER: _ClassVar[int]
    DESV_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    avg: float
    desv: float
    time: float
    def __init__(self, time: _Optional[float] = ..., avg: _Optional[float] = ..., desv: _Optional[float] = ...) -> None: ...
