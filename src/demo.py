import time
from pipeline import AxionPipeline

WATCH_FOLDER = "data/sample_docs"

def main():
    print("=== AXION AI Round-2 Demo (Prototype) ===")
    print("This demo shows LIVE updates from a folder (no re-indexing, no restart).")
    print("")
    print(f"1) Open this folder and create/edit .txt/.md/.log files: {WATCH_FOLDER}")
    print("2) Come back here and type a keyword query based on what you wrote.")
    print("3) Edit the file and run the same query again — the answer will change.")
    print("")

    pipeline = AxionPipeline(WATCH_FOLDER)

    # Initial scan
    a, u, r = pipeline.refresh()
    print(f"[Live Ingest] added={a}, updated={u}, removed={r}")
    print(pipeline.store.summary())
    print("")

    while True:
        try:
            query = input("Query (or 'rescan' / 'exit'): ").strip()
            if query.lower() in {"exit", "quit"}:
                print("Bye.")
                break

            if query.lower() == "rescan":
                a, u, r = pipeline.refresh()
                print(f"[Live Ingest] added={a}, updated={u}, removed={r}")
                print(pipeline.store.summary())
                continue

            # Auto refresh before answering (live behavior)
            pipeline.refresh()
            print("")
            print(pipeline.answer(query))
            print("\n---\n")

        except KeyboardInterrupt:
            print("\nBye.")
            break

if __name__ == "__main__":
    main()

