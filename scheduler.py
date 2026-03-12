from collections import defaultdict

CHANNELS = {
    "FAST": {"fee": 5, "capacity": 1, "latency": 3},
    "STANDARD": {"fee": 1, "capacity": 2, "latency": 5},
    "BULK": {"fee": 0.2, "capacity": 3, "latency": 8}
}

PENALTY = 0.001


class ChannelScheduler:

    def __init__(self, capacity, latency):

        self.capacity = capacity
        self.latency = latency
        self.timeline = defaultdict(int)

    def can_schedule(self,start):

        for t in range(start,start+self.latency):
            if self.timeline[t] >= self.capacity:
                return False

        return True


    def schedule(self,start):

        for t in range(start,start+self.latency):
            self.timeline[t] += 1


def schedule_transactions(transactions):

    schedulers = {
        c: ChannelScheduler(v["capacity"],v["latency"])
        for c,v in CHANNELS.items()
    }

    assignments=[]
    total_cost=0

    for tx in transactions:

        arrival = tx["arrival_time"]
        deadline = arrival + tx["max_delay"]

        best=None
        best_cost=float("inf")

        for cid,ch in CHANNELS.items():

            scheduler=schedulers[cid]

            for t in range(arrival,deadline):

                if not scheduler.can_schedule(t):
                    continue

                delay=t-arrival

                cost = ch["fee"] + delay * tx["amount"] * PENALTY

                if cost < best_cost:

                    best_cost=cost
                    best=(cid,t)

        if best:

            cid,start=best

            schedulers[cid].schedule(start)

            assignments.append({
                "tx_id":tx["tx_id"],
                "channel":cid,
                "start_time":start
            })

            total_cost += best_cost

    return assignments,total_cost
