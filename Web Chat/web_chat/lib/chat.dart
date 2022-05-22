import 'package:Secure_Chatting/streamsocket.dart';
import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'dart:io';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatRoom extends StatefulWidget {
  const ChatRoom({Key? key}) : super(key: key);

  @override
  State<ChatRoom> createState() => _ChatRoomState();
}

class _ChatRoomState extends State<ChatRoom> {
  final box = GetStorage();
  TextEditingController msgcontent = TextEditingController();
  StreamSocket streamSocket = StreamSocket();
  bool ciphered = false;
  @override
  Widget build(BuildContext context) {
    var username = box.read('username');
    var d = box.read('private_key');
    var N = box.read('n');
    var p = box.read('p');
    var q = box.read('q');
    IO.Socket socket = IO.io(
        'http://127.0.0.1:5000/',
        IO.OptionBuilder()
            .setTransports(['websocket']) // for Flutter or Dart VM
            .disableAutoConnect() // disable auto-connection
            .build());
    socket.connect();
    socket.onConnect((_) {
      print('connect');
    });

    var publicKey = box.read('public_key');
    var privateKey = box.read('private_key');
    var n = box.read('username');
    // implement Chat Room
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.indigo[500],
        title: const Text('Chat Room'),
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.lock_outline_rounded),
            onPressed: () {
              ciphered = !ciphered;
              setState(() {});
            },
          ),
        ],
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: Container(
              child: StreamBuilder<List>(
                stream: streamSocket.getResponse,
                builder: (context, AsyncSnapshot<List> snapshot) {
                  if (snapshot.hasData && snapshot.data != null) {
                    var messages = snapshot.data;
                    return ListView.builder(
                      reverse: true,
                      itemCount: messages?.length,
                      itemBuilder: (context, index) {
                        var info = messages?[index];
                        return Align(
                          alignment: username == info[0]
                              ? Alignment.centerRight
                              : Alignment.centerLeft,
                          child: Row(mainAxisSize: MainAxisSize.min, children: [
                            Card(
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(15.0),
                              ),
                              elevation: 2,
                              child: Padding(
                                padding: const EdgeInsets.all(18.0),
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  children: [
                                    Text(ciphered ? info[1] : info[1] ?? '...'),
                                    Text(
                                      info[0],
                                      style: TextStyle(
                                          fontSize: 10, color: Colors.grey),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ]),
                        );
                      },
                    );
                  } else {
                    return Center(child: Text("No Messages...Send any thing to trigger socket!",style: TextStyle(fontSize: 20,color: Colors.grey),));
                  }
                },
              ),
            ),
          ),
          Container(
            child: Row(
              children: <Widget>[
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.only(left: 18.0),
                    child: TextField(
                      controller: msgcontent,
                      decoration: InputDecoration(
                        hintText: 'Enter your message',
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: ElevatedButton(
                    child: Text('Send'),
                    onPressed: () async {
                      final Map<String, String> someMap = {
                        'username': username,
                        'message': msgcontent.text,
                      };
                      http
                          .post(Uri.parse("http://127.0.0.1:5000/sendmsg"),
                              headers: {"Content-Type": "application/json"},
                              body: jsonEncode(someMap))
                          .then((value) {
                        msgcontent.clear();
                        socket.emit("ihabsevent");

                        socket.emit("jemysevent");
                      });
                      if (username == "jemy") {
                        socket.on('jemymessage', (data) async {
                          var stringlist = data['yourmsgs'];
                          var list = List.from(stringlist.reversed);
                          List messages = [];
                          for (var i = 0; i < list.length; i++) {
                            int idx = list[i].indexOf(" ");
                            var info = [
                              list[i].substring(0, idx).trim(),
                              list[i].substring(idx + 1).trim()
                            ];
                            if (info[0] != username) {
                              final Map<String, String> someMap2 = {
                                'd': d,
                                'N': N,
                                'p': p,
                                'q': q,
                                'message': info[1],
                              };
                              var response = await http.post(
                                  Uri.parse("http://127.0.0.1:5000/decrypt"),
                                  headers: {"Content-Type": "application/json"},
                                  body: jsonEncode(someMap2));

                              dynamic resp = json.decode(response.body);
                              info[1] = resp['message'];

                              messages.add(info);
                            } else {
                              messages.add(info);
                            }
                          }

                          streamSocket.addResponse(messages);
                        });
                      } else {
                        socket.on('ihabmessage', (data) async {
                          var stringlist = data['yourmsgs'];
                          var list = List.from(stringlist.reversed);
                          List messages = [];
                          for (var i = 0; i < list.length; i++) {
                            int idx = list[i].indexOf(" ");
                            var info = [
                              list[i].substring(0, idx).trim(),
                              list[i].substring(idx + 1).trim()
                            ];
                            if (info[0] != username) {
                              final Map<String, String> someMap2 = {
                                'd': d,
                                'N': N,
                                'p': p,
                                'q': q,
                                'message': info[1],
                              };
                              var response = await http.post(
                                  Uri.parse("http://127.0.0.1:5000/decrypt"),
                                  headers: {"Content-Type": "application/json"},
                                  body: jsonEncode(someMap2));

                              dynamic resp = json.decode(response.body);
                              print("resp");
                              print(resp);
                              info[1] = resp['message'];
                              messages.add(info);
                            } else {
                              messages.add(info);
                            }
                          }

                          streamSocket.addResponse(messages);
                        });
                      }
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
