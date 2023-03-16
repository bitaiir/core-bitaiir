texto = "442db46ca1e922159529111533398760d19e46c5fa289d3d5a7b2bdbe6a15974"
bytes_texto = texto.encode("utf-8")

for b in bytes_texto:
    print("\\x" + format(b, "02x"), end="")
