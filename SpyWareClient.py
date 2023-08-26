import socket, sys

try:
    HOST = sys.argv[1]  # Replace with the server's IP address
except IndexError as e:
    print(f"You forgot to add the server as an argument.")
PORT = 12345


def get_file(conn, filename):
    conn.send(b"get_file")
    conn.send(filename.encode())

    response = conn.recv(1024)
    if response == b"File exists":
        with open(filename, 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
            print(f"File '{filename}' received successfully.")
    else:
        print(f"File '{filename}' not found on the server.")


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except NameError:
        print("Host wasn't defined.")
        exit()
    while True:
        print("Available commands:")
        print("1. get_file")
        print("2. exit")

        choice = input("Enter command number: ")

        if choice == "1":
            filename = input("Enter filename: ")
            get_file(client_socket, filename)
        elif choice == "2":
            print("Exiting the client.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    client_socket.close()


if __name__ == '__main__':
    main()
