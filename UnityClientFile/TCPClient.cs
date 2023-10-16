// Please note that I have not included any of the other Unity project files. I plan to release it once I have enough content for tutorials.
// I am using UTF-8 to be able to use Korean :) The fonts from the guide below are from google fonts api, and it has a decent catalog of fonts that you can use commercially. I wish I had found this earlier.
// ----- https://cho22.tistory.com/61

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System;
using System.Net.Sockets;
using System.Threading.Tasks;
using bluejayvrstudio;
using Newtonsoft.Json;

public class Player
{
    public string room_key;
    public string username;
    public string password;
    
    public Player(string _room_key, string _username, string _password)
    {
        room_key = _room_key;
        username = _username;
        password = _password;
    }
}

public class Message
{
    public string username;
    public string message;
    
    public Message(string _username, string _message)
    {
        username = _username;
        message = _message;
    }
}

public class TCPClient : MonoBehaviour
{
    [SerializeField] InputField RoomKey;
    [SerializeField] InputField Username;
    [SerializeField] Text outputText;

    [SerializeField] InputField UserReply; 

    [SerializeField] String server;
    
    private TcpClient currentClient;
    private NetworkStream currentStream;

    [SerializeField] GameObject messageTemplate;

    [SerializeField] GameObject JoinForm;
    [SerializeField] GameObject ChatInterface;

    private readonly object messageLock = new object();
    private string Replies="";

    private bool Entered = false;
    private bool Initiated = false;

    private string handshakeMessage = "";

    void Start()
    {
        // not sure if this is necessary, but better safe than sorry
        UserReply.text = "";
        
    }

    void Update()
    {
        lock (messageLock)
        {
            if (Replies != "")
            {
                Instantiate(messageTemplate, messageTemplate.transform.parent);
                var _reply = JsonConvert.DeserializeObject<Message>(Replies);
                messageTemplate.GetComponent<TMP_Text>().text = $"{_reply.username}: {_reply.message}";
                messageTemplate.transform.SetAsLastSibling();
                messageTemplate.SetActive(true);

                Debug.Log(Replies);
                Replies = "";
            }
        }

        if (handshakeMessage != "")
        {
            // outputText.text = handshakeMessage;
            if (handshakeMessage == "success")
            {
                JoinForm.SetActive(false);
                ChatInterface.SetActive(true);
                Entered = true;
                Debug.Log("Joining room!");
                handshakeMessage = "";
            }
            else
            {
                currentClient.Close();
                currentStream.Close();
                Debug.Log("Could not join the room. Please try again :(");
                handshakeMessage = "";
            }
        }

        if (Entered && !Initiated)
        {
            receive_message();
            Initiated = true;
        }

    }

    public async void test_button()
    {
        outputText.text = RoomKey.text + "  and  " + Username.text;
    }

    public async void receive_message()
    {
        async void some_task()
        {
            while (true)
            {
                if (currentStream != null)
                {
                    // Buffer to store the response bytes.
                    Byte[] data = new Byte[1024];

                    // String to store the response UTF8 representation.
                    String responseData = String.Empty;

                    // Read the first batch of the TcpServer response bytes.
                    Int32 bytes = currentStream.Read(data, 0, data.Length);
                    responseData = System.Text.Encoding.UTF8.GetString(data, 0, bytes);
                    Debug.Log($"Received: {responseData}");
                    while (true)
                    {
                        string temp = "";
                        lock (messageLock)
                        {
                            temp = String.Copy(Replies);
                        }
                        if (temp != "") await Task.Yield();
                        break;
                    }
                    lock (messageLock)
                    {
                        Replies = responseData;
                    }
                }
            }
        }
        Task.Run(() => some_task());
    }

    public async void send_message()
    {
        Instantiate(messageTemplate, messageTemplate.transform.parent);
        messageTemplate.GetComponent<TMP_Text>().text = $"Me: {UserReply.text}";
        messageTemplate.transform.SetAsLastSibling();
        messageTemplate.SetActive(true);

        if (currentStream != null)
        {
            var message = await CerealAsync.Serialize(new Message(Username.text, UserReply.text));
            Byte[] data = System.Text.Encoding.UTF8.GetBytes(message);

            currentStream.Write(data, 0, data.Length);

            UserReply.text = "";

            Debug.Log($"Sent: {message}");
        }
    }

    public async Task<string> Connect()
    {
        async Task<string> some_task()
        {
            try
            {
                // Create a TcpClient.
                // Note, for this client to work you need to have a TcpServer
                // connected to the same address as specified by the server, port
                // combination.
                Int32 port = 5000;

                TcpClient client = new TcpClient(server, port);
                currentClient = client;

                // Translate the passed message into UTF8 and store it as a Byte array.
                // Byte[] data = System.Text.Encoding.UTF8.GetBytes(message);
                var message = await CerealAsync.Serialize(new Player(RoomKey.text, Username.text, ""));
                Byte[] data = System.Text.Encoding.UTF8.GetBytes(message);


                // Get a client stream for reading and writing.
                NetworkStream stream = client.GetStream();
                currentStream = stream;

                // Send the message to the connected TcpServer.
                stream.Write(data, 0, data.Length);

                Debug.Log($"Sent: {message}");

                // Receive the server response.

                // Buffer to store the response bytes.
                data = new Byte[1024];
                String responseData = String.Empty;

                Int32 bytes = stream.Read(data, 0, data.Length);
                responseData = System.Text.Encoding.UTF8.GetString(data, 0, bytes);
                Debug.Log($"Received: {responseData}");
                
                if (responseData == "success")
                {
                    Debug.Log("joining room :D");
                    return "success";
                }
                else
                {
                    stream.Close();
                    client.Close();
                    Debug.Log(responseData);
                    return responseData;
                }
            }
            catch (ArgumentNullException e)
            {
                Debug.Log($"ArgumentNullException: {e}");
                return "Unable to connect to the server :(";
            }
            catch (SocketException e)
            {
                Debug.Log($"SocketException: {e}");
                return "Unable to connect to the server :(";
            }
            return "Unable to connect to the server :(";
        }
        string result = await Task.Run(async () => await some_task());
        return result;
    }

    public async void ConnectWrapper()
    {
        var result = await Connect();
        handshakeMessage = String.Copy(result);
        outputText.text = handshakeMessage;
    }
}
