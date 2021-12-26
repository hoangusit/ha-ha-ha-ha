       try:
            msg = receive_msg(conn)
            print(msg)
            if msg == "sign in" : signin(conn)
            elif msg == "sign up": signup(conn)
            elif msg == DISCONNECT_MESSAGE:
                connected = False
        except:
            connected = False