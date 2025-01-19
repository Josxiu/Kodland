import time

start = time.time()
# Código que quieres medir
for i in range(1000000):
    x = i + 1
end = time.time()
print(f"Duración: {end - start} segundos")
