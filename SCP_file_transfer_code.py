 def send_file(local_path, remote_path, hostname, port, username, password):
        """
        Uploads a file from the local machine to a remote server using SCP (Secure Copy Protocol).

        Parameters:
        - local_path: The path to the local file to be uploaded.
        - remote_path: The destination path on the remote server.
        - hostname: The hostname or IP address of the remote server.
        - port: The SSH port of the remote server.
        - username: The username used for authentication.
        - password: The password used for authentication.

        Returns:
        None
        """
        scp = None

        try:
            # Create an SSH client
            ssh_client = paramiko.SSHClient()
            # Automatically add the server's host key
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the server
            ssh_client.connect(hostname, port=port, username=username, password=password)

            # Create an SCP client
            scp = ssh_client.open_sftp()

            # Upload the file
            scp.put(local_path, remote_path)

            print(f"File '{local_path}' uploaded to '{remote_path}' successfully.")
        except Exception as e:
            print(f"Error uploading file: {e}")
        finally:
            if scp:
                # Close the SCP connection
                scp.close()
            # Close the SSH connection
            ssh_client.close()
