"""CMIP6-decadal fix modules."""

from .cmip6d_0001_time_meta import DecadalTimeMetadata  # noqa: F401
from .cmip6d_0002_calendar import DecadalCalendarNormalization  # noqa: F401
from .cmip6d_0003_realization_var import DecadalRealizationVariable  # noqa: F401
from .cmip6d_0004_coord_encoding import DecadalCoordinatesEncodingCleanup  # noqa: F401
from .cmip6d_0005_realization_comment import DecadalRealizationCommentNormalization  # noqa: F401
from .cmip6d_0006_realization_dtype import DecadalRealizationDtypeNormalization  # noqa: F401
from .cmip6d_0007_fillvalue_encoding import DecadalFillValueEncodingCleanup  # noqa: F401
from .cmip6d_0008_info_url import DecadalFurtherInfoUrlNormalization  # noqa: F401
from .cmip6d_0009_start_token import DecadalStartTokenNormalization  # noqa: F401
from .cmip6d_0010_realization_name import DecadalRealizationLongNameNormalization  # noqa: F401
from .cmip6d_0011_realization_index import DecadalRealizationIndexNormalization  # noqa: F401
from .cmip6d_0012_leadtime_meta import DecadalLeadtimeMetadataNormalization  # noqa: F401
from .cmip6d_0013_model_attrs import DecadalModelGlobalAttributes  # noqa: F401
from .cmip6d_0014_reftime_coord import DecadalReftimeCoordinate  # noqa: F401
from .cmip6d_0015_leadtime_coord import DecadalLeadtimeCoordinate  # noqa: F401
