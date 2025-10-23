import tiktoken
enc=tiktoken.encoding_for_model("gpt-4o")

token=enc.encode("who are you man")
print(token)
decodedText=enc.decode(token)
print(decodedText)







