# enumerate coords in rings 1..n-1; this doesn't work for the origin
for ring in range(1,4):
    # start in the upper right corner ...
    (x,y,z) = (0,-ring,ring)
    # ... moving clockwise (south-east, or +x,-z)
    move = [1,0,-1]         

    # each ring has six more coordinates than the last
    for i in range(6*ring):
        # print first to get the starting hex for this ring
        print "%d/%d: (%d,%d,%d) " % (ring,i,x,y,z)
        # then move to the next hex
        (x,y,z) = map(sum, zip((x,y,z), move))

        # when a coordinate has a zero in it, we're in a corner of
        # the ring, so we need to turn right
        if 0 in (x,y,z):
            # left shift the zero through the move vector for a
            # right turn
            i = move.index(0)
            (move[i-1],move[i]) = (move[i],move[i-1])

    print # blank line between rings
