# JSON Command


## jq

- Install

```bash
sudo apt-get install jq 
```

- 整形

```bash
% echo '{"name":"Alice","age":30}' | jq .
{
  "name": "Alice",
  "age": 30
}
```

- 抽出

```bash
% echo '{"name":"Alice","age":30}' | jq .name
"Alice"
```

- 配列から秀出

```bash
% echo '[{"id":1,"name":"A"},{"id":2,"name":"B"}]' | jq '.[].name'
"A"
"B"
```

- 追加

```bash
% echo '{"name":"Alice"}' | jq '.age = 30'
{
  "name": "Alice",
  "age": 30
}
```


## jc

- Install

```bash
sudo apt-get install jc
```

- ls

```bash
% ls -l | jc --ls | jq .                  
[
  {
    "filename": "angular/",
    "flags": "drwxr-xr-x",
    "links": 7,
    "owner": "yo4taka",
    "group": "staff",
    "size": 224,
    "date": "2 11 2023",
    "epoch": null,
    "epoch_utc": null
  },
]
```

## jo

- Install

```bash
sudo apt-get install jo 
```

- 作成
```bash
% jo name="Taro" age=25 city="Tokyo"
{"name":"Taro","age":25,"city":"Tokyo"}
```

- 配列

```bash
% jo -a item1 item2 item3
["item1","item2","item3"]
```

- オブジェクト

```bash
% jo user=$(jo id=1 name="Alice") status="active"
{"user":{"id":1,"name":"Alice"},"status":"active"}
```

- 配列とオブジェクト

```bash
% jo users=$(jo -a $(jo name=Alice age=30) $(jo name=Bob age=25))
{"users":[{"name":"Alice","age":30},{"name":"Bob","age":25}]}
```