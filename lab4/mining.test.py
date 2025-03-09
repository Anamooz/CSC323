from statistics import mean

previousBlockId = "12345"

megaHashes = {}

trails = [5000000]

for trials in trails:

    results = []
    for i in range(5):
        start = time.perf_counter()
        nonce, attempts = hashGPU(
            json.dumps(example_transaction, sort_keys=True), previousBlockId, trials
        )
        end = time.perf_counter()
        megaHash = attempts / (end - start) / 1000000
        results.append(megaHash)
    megaHashes[trials] = mean(results)
    print("MegaHashes per second: ", megaHashes[trials], "for", trials, "trials")

# Sort results by value
megaHashes = dict(sorted(megaHashes.items(), key=lambda item: item[1]))
print(megaHashes)
