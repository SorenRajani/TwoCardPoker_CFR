from two_card_poker import poker_bot
import time
import sys
import pickle

if __name__ == "__main__":
    time1 = time.time()
    trainer = poker_bot()
    trainer.train(n_iter=10**8)
    print(abs(time1 - time.time()))
    print(sys.getsizeof(trainer))

    # Saving the model
    with open("save.p", "wb") as f:
        pickle.dump(trainer, f)
