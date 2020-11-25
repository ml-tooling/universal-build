<!-- markdownlint-disable -->

<a href="https://github.com/mltooling/project-template/blob/main/examples/python-lib/src/template_package/api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `template_package.api`





---

<a href="https://github.com/mltooling/project-template/blob/main/examples/python-lib/src/template_package/api.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `read_item`

```python
read_item(item_id: int, q: Optional[str] = None) → dict
```






---

<a href="https://github.com/mltooling/project-template/blob/main/examples/python-lib/src/template_package/api.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_item`

```python
update_item(item_id: int, item: Item) → dict
```






---

<a href="https://github.com/mltooling/project-template/blob/main/examples/python-lib/src/template_package/api.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ext_call`

```python
ext_call() → dict
```






---

<a href="https://github.com/mltooling/project-template/blob/main/examples/python-lib/src/template_package/api.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `slow_call_to_external_url`

```python
slow_call_to_external_url() → dict
```






---

<a href="https://github.com/mltooling/project-template/blob/main/examples/python-lib/src/template_package/api.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Item`




#### <kbd>property</kbd> fields






### <kbd>function</kbd> `__init__`

```python
__init__(__pydantic_self__, **data: Any) → None
```

Create a new model by parsing and validating input data from keyword arguments. 

Raises ValidationError if the input data cannot be parsed to form a valid model. 


#### <kbd>handler</kbd> copy

#### <kbd>handler</kbd> dict

#### <kbd>handler</kbd> json

#### <kbd>handler</kbd> to_string


---

### <kbd>classmethod</kbd> `construct`

```python
construct(
    _fields_set: Optional[ForwardRef('SetStr')] = None,
    **values: Any
) → Model
```

Creates a new model setting __dict__ and __fields_set__ from trusted or pre-validated data. Default values are respected, but no other validation is performed. 

---

### <kbd>classmethod</kbd> `from_orm`

```python
from_orm(obj: Any) → Model
```





---

### <kbd>classmethod</kbd> `parse_file`

```python
parse_file(
    path: Union[str, Path],
    content_type: 'unicode' = None,
    encoding: 'unicode' = 'utf8',
    proto: Protocol = None,
    allow_pickle: bool = False
) → Model
```





---

### <kbd>classmethod</kbd> `parse_obj`

```python
parse_obj(obj: Any) → Model
```





---

### <kbd>classmethod</kbd> `parse_raw`

```python
parse_raw(
    b: Union[str, bytes],
    content_type: 'unicode' = None,
    encoding: 'unicode' = 'utf8',
    proto: Protocol = None,
    allow_pickle: bool = False
) → Model
```





---

### <kbd>classmethod</kbd> `schema`

```python
schema(
    by_alias: bool = True,
    ref_template: 'unicode' = '#/definitions/{model}'
) → DictStrAny
```





---

### <kbd>classmethod</kbd> `schema_json`

```python
schema_json(
    by_alias: bool = True,
    ref_template: 'unicode' = '#/definitions/{model}',
    **dumps_kwargs: Any
) → unicode
```





---

### <kbd>classmethod</kbd> `update_forward_refs`

```python
update_forward_refs(**localns: Any) → None
```

Try to update ForwardRefs on fields based on this Model, globalns and localns. 

---

### <kbd>classmethod</kbd> `validate`

```python
validate(value: Any) → Model
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
