corpus = {"key1": {"key2", "key3"}, "key2": {"key3"}, "key3": set()}
for key in corpus:
    if not corpus[key]:
        set_of_keys = {key1 for key1 in corpus}
        corpus[key].update(set_of_keys)

print(corpus)
