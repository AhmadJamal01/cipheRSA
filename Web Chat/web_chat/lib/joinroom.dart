import 'package:Secure_Chatting/chat.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
class JoinRoom extends StatelessWidget {
  JoinRoom({Key? key}) : super(key: key);
  TextEditingController roomname = TextEditingController();
  TextEditingController username = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
      child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextFormField(
              controller: roomname,
              decoration: InputDecoration(
                labelText: "Room name",
                labelStyle: TextStyle(
                  color: Colors.indigo[200],
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
                floatingLabelBehavior: FloatingLabelBehavior.auto,
                hintText: "Room name",
                hintStyle: TextStyle(color: Colors.grey[600]),
                fillColor: Colors.grey[100],
                filled: true,
                contentPadding: EdgeInsets.all(12.0),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.grey[300]!, width: 2.0),
                ),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blue, width: 2.0),
                ),
              ),
            ),
            SizedBox(
              height: 20,
            ),
            TextFormField(
              controller: username,
              decoration: InputDecoration(
                labelText: "Username",
                labelStyle: TextStyle(
                  color: Colors.indigo[200],
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
                floatingLabelBehavior: FloatingLabelBehavior.auto,
                hintText: "Username",
                hintStyle: TextStyle(color: Colors.grey[600]),
                fillColor: Colors.grey[100],
                filled: true,
                contentPadding: EdgeInsets.all(12.0),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.grey[300]!, width: 2.0),
                ),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blue, width: 2.0),
                ),
              ),
            ),
            SizedBox(
              height: 20,
            ),
            ElevatedButton(
              child: Text('Join'),
              onPressed: () async {
                final Map<String, String> someMap = {
                  'username': username.text,
                  'channel': roomname.text,
                };
                http
                    .post(Uri.parse("http://127.0.0.1:5000/channels"),
                        headers: {"Content-Type": "application/json"},
                        body: jsonEncode(someMap))
                    .then((response) async {
                  dynamic resp = json.decode(response.body);
                  if (resp['Error'] == "None") {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) =>ChatRoom()));
                  } else {
                    print(resp['Error']);
                  }
                });
              },
            ),
          ]),
    ));
  }
}