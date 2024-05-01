# Generate two lists

import random

import copy

class ListGen():
    def __init__(self, l):
        self.n = -1
        self.l = l
    def get_next_element(self):
        if self.n + 1 < len(self.l):
            self.n += 1
            return self.l[self.n]
        else:
            self.n +=1
            return None
    def get_next_element_pair(self):
        if self.n + 1 < len(self.l):
            self.n += 1
            return self.l[self.n], self.n
        else:
            self.n +=1
            return None

    def move_head(self, n):
        self.n = n

    def move_head_relative(self, n):
        self.n += n
    
    def get_value_at(self, n):
        if n < len(self.l):
            return self.l[n]
        else:
            return None
    
    def peek(self):
        if self.n < len(self.l):
            return self.l[self.n]
        else:
            return None
    def peek_ahead(self, n):
        if self.n + n < len(self.l):
            return self.l[self.n + n]
        else:
            return None
    
    def current_index(self):
        return self.n

    def __len__(self):
        return len(self.l)

    def is_empty(self):
        return self.n >= len(self.l)

    def __str__(self):
        return str(self.l)


DONE = 0
NO_COLLISION = 1
COLLISION = 2
MAYBE_COLLISION = 3
class Collider():
    def __init__(self, left : ListGen, right : ListGen):
        self.left = left
        self.right = right
        self.cycles = 0
        self.left.get_next_element()
        self.right.get_next_element()
        self.ops = 0

    def get_next_collision(self, left, right):
        # Normally it's just 
        self.cycles += 1
        if left.is_empty() or right.is_empty():
            return DONE
        elif left.peek() < right.peek():
            left.get_next_element()
            return NO_COLLISION
        elif left.peek() > right.peek():
            right.get_next_element()
            return NO_COLLISION
        else:
            left.get_next_element()
            right.get_next_element()
            return COLLISION

    def cycles_for_all_collisions(self):
        while True:
            result = self.get_next_collision(self.left, self.right)
            if result == DONE:
                return self.cycles
            if result == COLLISION:
                self.ops += 1

# Section 5.2 of the paper
# Basically you set up a bunch of checkpoints, so when you want to skip to a value, you can avoid reading some stuff.
class Collider_with_skip():
    
    def __init__(self, left : ListGen, right : ListGen, T: int):
        self.left = left
        self.right = right
        self.cycles = 0
        # For now just assume S > T. It's reasonable I guess.
        # indices are
        self.left_indices = [int(i*len(left)/(T+1)) for i in range(1, T+1)]
        self.right_indices = [int(i*len(right)/(T+1)) for i in range(1, T+1)]
        self.left_values = [(i, left.get_value_at(i)) for i in self.left_indices]
        self.right_values = [(i, right.get_value_at(i)) for i in self.right_indices]
        self.left.get_next_element()
        self.right.get_next_element()


    def get_next_collision(self, left, right):
        # Normally it's just 
        self.cycles += 1
        if left.is_empty() or right.is_empty():
            return DONE
        elif left.peek() < right.peek():
            # advance L up to the next checkpoint if possible
            # This operation is done in one cycle in the hardware implementation
            min_index_with_checkpoint = list(filter(lambda x: x[1] <= right.peek(), self.left_values))
            if len(min_index_with_checkpoint) > 0 and left.current_index() < min_index_with_checkpoint[-1][0]:
                left.move_head(min_index_with_checkpoint[-1][0])
            else:
                left.get_next_element()
            return MAYBE_COLLISION
        elif left.peek() > right.peek():
            # This operation is done in one cycle in the hardware implementation
            min_index_with_checkpoint = list(filter(lambda x: x[1] <= left.peek(), self.right_values))
            if len(min_index_with_checkpoint) > 0 and right.current_index() < min_index_with_checkpoint[-1][0]:
                right.move_head(min_index_with_checkpoint[-1][0])
            else:
                right.get_next_element()
            return MAYBE_COLLISION
        else:
            left.get_next_element()
            right.get_next_element()
            return COLLISION

    def cycles_for_all_collisions(self):
        while True:
            if self.get_next_collision(self.left, self.right) == DONE:
                return self.cycles

# In here the trick is to store the next N elements with offsets of like K or something. This will speed you up because science.
# One option is to skip over by some fraction of things.

# Another option to get rid of the crazy O(N) dependence is to use the double banking more effectively.
# so if you increase, you just fill in one of your additional values.

class Custom_collider_lookahead():
    def __init__(self, left : ListGen, right : ListGen, lookahead: int):
        self.left = left
        self.right = right
        self.cycles = 0
        # For now just assume S > T. It's reasonable I guess.
        # indices are
        self.lookahead = lookahead
        self.left.get_next_element()
        self.right.get_next_element()
        self.logged_skips = []

    def get_next_collision(self, left, right):
        # Normally it's just 
        self.cycles += 1
        if left.is_empty() or right.is_empty():
            return DONE
        elif left.peek() < right.peek():
            # Look ahead 5 elements if possible
            # advance L up to the next checkpoint if possible
            # This operation is done in one cycle in the hardware implementation
            for i in range(self.lookahead, 1, -1):
                if left.peek_ahead(i) is not None and left.peek_ahead(i-1) <= right.peek():
                    # print("Moving left by", i, "at ", left.peek())
                    self.logged_skips.append(i)
                    left.move_head_relative(i)
                    # self.cycles += 1
                    return MAYBE_COLLISION
            # if left.peek_ahead(self.lookahead) is not None and left.peek_ahead(self.lookahead) < right.peek():
            #     print("Moving left")
            #     left.move_head_relative(self.lookahead)
            # else:
            self.logged_skips.append(1)
            left.get_next_element()
            return NO_COLLISION
        elif left.peek() > right.peek():
            # This operation is done in one cycle in the hardware implementation
            for i in range(self.lookahead, 1, -1):
                if right.peek_ahead(i) is not None and right.peek_ahead(i-1) <= left.peek():
                    # print("Moving right by", i , "at", right.peek())
                    self.logged_skips.append(i)
                    right.move_head_relative(i)
                    # self.cycles += 1
                    return MAYBE_COLLISION
            # if right.peek_ahead(self.lookahead) is not None and right.peek_ahead(self.lookahead) < left.peek():
            #     print("Moving right")
            #     right.move_head_relative(self.lookahead)
            # else:
            self.logged_skips.append(1)
            right.get_next_element()
            return NO_COLLISION
        else:
            self.logged_skips.append(1)
            left.get_next_element()
            right.get_next_element()
            return COLLISION

    def cycles_for_all_collisions(self):
        while True:
            if self.get_next_collision(self.left, self.right) == DONE:
                return self.cycles

    def get_skips(self):
        return self.logged_skips

class NextNStorer():
    def __init__(self, T, stream):
        self.N = 0
        self.stream = stream
        self.values = [(None, None) for i in range(T)] # Index, value
        self.enq_next_val()

    def get_final_index_less_than(self, value):
        min_index = list(filter(lambda x: x[1] < value, self.values))
        if len(min_index) > 0:
            return min_index[-1][0]
        else:
            return None
    
    def enq_new_value(self, index, value):
        self.values = self.values[1:] +[(index, value)]

    def enq_next_val(self):
        # -1 since its only called when N is incremented
        isDone = self.stream.get_next_element_pair()
        if isDone == None:
            return
        el, idx = isDone
        # assert(idx == self.N - 1)
        self.enq_new_value(idx, el)

    def get_next_element(self):
        # If N+1 is stored in our values array, then return that
        self.N += 1
        if self.N >= len(self.stream):
            return None

        # Get the indices
        indices = {i[0] : i[1] for i in self.values}
        # If we have this value stored, the use that, and then enq the next value into our values array
        if self.N in indices:
            result =  indices[self.N]
            self.enq_next_val()
            return result
        else:
            # Enq the next value into our values array (since we MUST be behind the mark)
            self.enq_next_val()
            return self.peek()

    def is_empty(self):
        return self.N >= len(self.stream)

    def peek(self):
        if self.N > len(self.stream):
            return None
        indices = {i[0] : i[1] for i in self.values}
        if self.N in indices:
            return indices[self.N]
        else:
            print(self.N)
            print(self.values)
            # throw an exception
            print("Peek should always work")
            # print the traceback
            import traceback
            traceback.print_stack()
            raise

    def refill(self):
        # if the bottom element is < than N, then we need to refill by one value
        if self.values[0][0] is None or self.values[0][0] < self.N:
            self.enq_next_val()

    def move_to_first_index_after(self, value):
        og = self.N
        viable_elements = list(filter(lambda x: x[0] is not None and x[1] >= value, self.values))
        if len(viable_elements) > 0:
            result =  viable_elements[0][0]
            if (result > self.N):
                self.N = result
                self.enq_next_val()
                return self.N - og
            else:
                return None
        else:
            # Else just move to the final element
            if (self.values[-1][1] < value and self.N < self.values[-1][0]):
                self.N = self.values[-1][0]
                self.enq_next_val()
                return self.N - og
            return None



class Custom_collider_assoc_lookahead():
    def __init__(self, left : ListGen, right : ListGen, lookahead: int):
        # self.left = left
        # self.right = right
        # For now just assume S > T. It's reasonable I guess.
        # indices are
        self.lookahead = lookahead
        self.left_storer = NextNStorer(lookahead, left)
        self.right_storer = NextNStorer(lookahead, right)
        self.cycles = 0
        for i in range(lookahead):
            self.left_storer.refill()
            self.right_storer.refill()    
        self.logged_skips = []

    def get_next_collision(self):
        # Normally it's just 
        self.cycles += 1
        if self.left_storer.is_empty() or self.right_storer.is_empty():
            return DONE
        elif self.left_storer.peek() < self.right_storer.peek():
            # Look ahead 5 elements if possible
            # advance L up to the next checkpoint if possible
            # This operation is done in one cycle in the hardware implementation
            self.right_storer.refill()
            skipped = self.left_storer.move_to_first_index_after(self.right_storer.peek())
            if (skipped is not None):
                self.logged_skips.append(skipped)
                return MAYBE_COLLISION
            else:
                self.logged_skips.append(1)
                self.left_storer.get_next_element()
        elif self.left_storer.peek() > self.right_storer.peek():
            # This operation is done in one cycle in the hardware implementation
            self.left_storer.refill()
            skipped =  self.right_storer.move_to_first_index_after(self.left_storer.peek())
            if (skipped is not None):
                self.logged_skips.append(skipped)
                return MAYBE_COLLISION
            else:
                self.logged_skips.append(1)
                self.right_storer.get_next_element()
                return NO_COLLISION
        else:
            self.logged_skips.append(1)
            self.left_storer.get_next_element()
            self.right_storer.get_next_element()
            return COLLISION

    def cycles_for_all_collisions(self):
        while True:
            if self.get_next_collision() == DONE:
                return self.cycles
    def get_skips(self):
        return self.logged_skips





# The idea is we can maybe buffer each thing. Hash it and shove it into buckets. Then look within that bucket.
# Currently we can only look at one thing per cycle.
# And then just fucking run it down like a retard

def genList(length, density):
    uncompressed = [0] * length

    for i in range(length):
        if random.random() < density:
            uncompressed[i] = i

    # Then filter out all the zeros
    return list(filter(lambda x: x != 0, uncompressed))

COLLIDER = 0
SKIP = 1
LOOKAHEAD = 2
ASSOC = 3
collider_names = {COLLIDER : 'classic', SKIP : 'extensor (with skip optimizations)', LOOKAHEAD : 'our custom version (lookahead)', ASSOC : 'hardware friendy lookahead'}
def test_matmul(densityA, densityB, M, K, N):
    print("Simulating a matmul with parameters densityA", densityA, "densityB", densityB, "A =", [M, K], "B =", [K, N])
    print("Algorithmic ops: ", M*K*N)
    A = []
    B = []
    for i in range(M):
        A.append(genList(K, densityA))
    for i in range(N):
        B.append(genList(K, densityB))

    
    for collider in [COLLIDER, SKIP, LOOKAHEAD, ASSOC]:
        cycles=0
        computes=0
        for left in A:
            for right in B:
                if collider == COLLIDER:
                    c = Collider(ListGen(left), ListGen(right))
                if collider == SKIP:
                    c = Collider_with_skip(ListGen(left), ListGen(right), 10)
                if collider == LOOKAHEAD:
                    c = Custom_collider_lookahead(ListGen(left), ListGen(right), 10)
                if collider == ASSOC:
                    c = Custom_collider_assoc_lookahead(ListGen(left), ListGen(right), 10)
                cycles += c.cycles_for_all_collisions()
                if collider == COLLIDER:
                    computes+=c.ops
        if (collider == COLLIDER):
            print("Real computes:" ,computes)
        print(collider_names[collider], ":", cycles, "cycles")
    
def test_skips(densityA, densityB, M, K, N, T, N1, N2):
    print("Simulating a matmul with parameters densityA", densityA, "densityB", densityB, "A =", [M, K], "B =", [K, N])
    print("Algorithmic ops: ", M*K*N)
    A = []
    B = []
    for i in range(M):
        A.append(genList(K, densityA))
    for i in range(N):
        B.append(genList(K, densityB))

    results = []
    
    for collider in [LOOKAHEAD, ASSOC]:
        skips=[]
        for left in A:
            for right in B:
                if collider == COLLIDER:
                    c = Collider(ListGen(left), ListGen(right))
                if collider == SKIP:
                    c = Collider_with_skip(ListGen(left), ListGen(right), T)
                if collider == LOOKAHEAD:
                    c = Custom_collider_lookahead(ListGen(left), ListGen(right), N1)
                if collider == ASSOC:
                    c = Custom_collider_assoc_lookahead(ListGen(left), ListGen(right), N2)
                c.cycles_for_all_collisions()
                skips += c.get_skips()
        print(collider_names[collider], ":", skips, "skips")
        results.append((collider, skips))

    return results


def test_matmul(densityA, densityB, M, K, N, T, N1, N2):
    print("Simulating a matmul with parameters densityA", densityA, "densityB", densityB, "A =", [M, K], "B =", [K, N])
    print("Algorithmic ops: ", M*K*N)
    A = []
    B = []
    for i in range(M):
        A.append(genList(K, densityA))
    for i in range(N):
        B.append(genList(K, densityB))

    results = []
    
    for collider in [COLLIDER, SKIP, LOOKAHEAD, ASSOC]:
        cycles=0
        computes=0
        for left in A:
            for right in B:
                if collider == COLLIDER:
                    c = Collider(ListGen(left), ListGen(right))
                if collider == SKIP:
                    c = Collider_with_skip(ListGen(left), ListGen(right), T)
                if collider == LOOKAHEAD:
                    c = Custom_collider_lookahead(ListGen(left), ListGen(right), N1)
                if collider == ASSOC:
                    c = Custom_collider_assoc_lookahead(ListGen(left), ListGen(right), N2)
                cycles += c.cycles_for_all_collisions()
                if collider == COLLIDER:
                    computes+=c.ops
        if (collider == COLLIDER):
            print("Real computes:" ,computes)
        print(collider_names[collider], ":", cycles, "cycles")
        results.append((collider, cycles))

    return results

    

if __name__ == '__main__':
    left = (genList(100, 0.5))
    right = (genList(100, 0.5))
    print(left)
    print(right)

    c = Collider(ListGen(left), ListGen(right))
    print(c.cycles_for_all_collisions())
    c = Collider_with_skip(ListGen(left), ListGen(right), 10)
    print(c.cycles_for_all_collisions())
    c = Custom_collider_lookahead(ListGen(left), ListGen(right), 10)
    print(c.cycles_for_all_collisions())

    c = Custom_collider_assoc_lookahead(ListGen(left), ListGen(right), 10)
    print(c.cycles_for_all_collisions())

    test_matmul(0.25, 0.5,80, 90, 80)
    test_matmul(0.25, 0.5,8, 900, 8)

