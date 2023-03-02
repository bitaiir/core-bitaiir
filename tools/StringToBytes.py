texto = "bitaiir"
bytes_texto = texto.encode("utf-8")

for b in bytes_texto:
    print("\\x" + format(b, "02x"), end="")
