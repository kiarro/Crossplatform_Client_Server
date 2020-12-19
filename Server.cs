using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using NLog;

namespace SocketTcpServer {
    class Server {
        int port = 11000; // server port

        RequestProcessor rprocessor = new RequestProcessor();

        /// <summary>
        /// Server object, that listen for clients
        /// address = 192.168.1.130 (local network)
        /// port = 11000
        /// </summary>
        /// <value></value>
        Server(string address = "192.168.31.130", string pathFunc = null, string pythonPath = "I:\\Python\\python.exe") {
            // get address
            if (!(pathFunc is null))
                RequestProcessor.pathToProc = pathFunc;
            RequestProcessor.pathPython = pythonPath;
            IPAddress ipAddress = new IPAddress(address.Split('.').Select(x => Byte.Parse(x)).ToArray());
            IPEndPoint ipPoint = new IPEndPoint(ipAddress, port);

            // create socket
            Socket listenSocket = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            try {
                // bind socket with end point
                listenSocket.Bind(ipPoint);

                // listen (max connections = 10)
                listenSocket.Listen(10);

                Console.WriteLine("Server started. Waiting connections...");

                while (true) {
                    Socket handler = listenSocket.Accept();

                    new Task(() => { ProcessClient(handler); }).Start();
                }
            } catch (Exception ex) {
                Console.WriteLine(ex.Message);
            }

        }

        private void ProcessClient(Socket handler) {
            StringBuilder builder = new StringBuilder();
            Console.WriteLine("Connection accepted.");

            Logger logger = LogManager.GetCurrentClassLogger();

            int bytes = 0;
            byte[] buffer = new byte[1024];

            // receive bytes
            do {
                bytes = handler.Receive(buffer);
                builder.Append(Encoding.Unicode.GetString(buffer, 0, bytes));
                logger.Debug("bytes: {0}",Encoding.Unicode.GetString(buffer, 0, bytes));
                logger.Debug("builder: ",builder.ToString());
                logger.Debug("builder[-1]: {0}, builder[-2]: {1}", builder[builder.Length-1], builder[builder.Length-2]);
            }
            while (builder[builder.Length-1]!='\u0000' || builder[builder.Length-2]!='\u0000');
            builder.Remove(builder.Length-2, 2);
            string request = builder.ToString();
            Console.WriteLine(DateTime.Now.ToString("HH:mm:ss.fff") + " <= " + request);
            logger.Info(" <= " + request);
            // process request
            string response = ProcessRequest(request);
            response += "\u0000\u0000" ; // end sequence
            // send response
            buffer = Encoding.Unicode.GetBytes(response);
            handler.Send(buffer);

            Console.WriteLine(DateTime.Now.ToString("HH:mm:ss.fff") + " => " + response);
            logger.Info(" => " + response);
            // close socket
            handler.Shutdown(SocketShutdown.Both);
            handler.Close();
        }

        private string ProcessRequest(string request) {
            string response = rprocessor.ProcessRequest(request);
            // process client request

            return response;
        }

        static void Main(string[] args) {
            Console.WriteLine("Program started with args " + String.Join(" ", args));
            Server server;
            if (args.Length > 0)
                server = new Server(args[0]);
            else
                server = new Server();

        }
    }
}
