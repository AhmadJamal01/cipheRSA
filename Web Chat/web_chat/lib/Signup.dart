import 'dart:convert';

import 'package:Secure_Chatting/into.dart';
import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:http/http.dart' as http;
import 'package:Secure_Chatting/chat.dart';


class SignUp extends StatefulWidget {
  SignUp({Key? key}) : super(key: key);

  @override
  State<SignUp> createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  TextEditingController pfield = TextEditingController();

  TextEditingController qfield = TextEditingController();

  TextEditingController efield = TextEditingController();
  TextEditingController username = TextEditingController();

  String errormsg ="";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        // take screen width and height
        width: MediaQuery.of(context).size.width,
        height: MediaQuery.of(context).size.height,
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/images/background.jpg"),
            fit: BoxFit.cover,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.only(right: 180.0),
          child: Align(
            alignment: Alignment.centerRight,
            child: SizedBox(
              width: 300,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text(
                    'Choose your parameters',
                    style: TextStyle(
                      fontSize: 20,
                      color: Colors.white,
                      fontWeight: FontWeight.w400,
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
                        borderSide:
                            BorderSide(color: Colors.grey[300]!, width: 2.0),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Colors.blue, width: 2.0),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  // TextField
                  TextFormField(
                    controller: pfield,
                    decoration: InputDecoration(
                      labelText: "P",
                      labelStyle: TextStyle(
                        color: Colors.indigo[200],
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                      ),
                      floatingLabelBehavior: FloatingLabelBehavior.auto,
                      hintText: "P",
                      hintStyle: TextStyle(color: Colors.grey[600]),
                      fillColor: Colors.grey[100],
                      filled: true,
                      contentPadding: EdgeInsets.all(12.0),
                      enabledBorder: OutlineInputBorder(
                        borderSide:
                            BorderSide(color: Colors.grey[300]!, width: 2.0),
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
                    controller: qfield,
                    decoration: InputDecoration(
                      labelText: "q",
                      labelStyle: TextStyle(
                        color: Colors.indigo[200],
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                      ),
                      floatingLabelBehavior: FloatingLabelBehavior.auto,
                      hintText: "q",
                      hintStyle: TextStyle(color: Colors.grey[600]),
                      fillColor: Colors.grey[100],
                      filled: true,
                      contentPadding: EdgeInsets.all(12.0),
                      enabledBorder: OutlineInputBorder(
                        borderSide:
                            BorderSide(color: Colors.grey[300]!, width: 2.0),
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
                    controller: efield,
                    decoration: InputDecoration(
                      labelText: "e",
                      labelStyle: TextStyle(
                        color: Colors.indigo[200],
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                      ),
                      floatingLabelBehavior: FloatingLabelBehavior.auto,
                      hintText: "e",
                      hintStyle: TextStyle(color: Colors.grey[600]),
                      fillColor: Colors.grey[100],
                      filled: true,
                      contentPadding: EdgeInsets.all(12.0),
                      enabledBorder: OutlineInputBorder(
                        borderSide:
                            BorderSide(color: Colors.grey[300]!, width: 2.0),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Colors.blue, width: 2.0),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Text(errormsg , style: TextStyle(color: Colors.red),),
                  SizedBox(
                    height: 20,
                  ),
                  ElevatedButton(
                    child: Text('Sign Up'),
                    onPressed: () async {
                      final Map<String, String> someMap = {
                        'username': username.text,
                        'p': pfield.text,
                        'q': qfield.text,
                        'e': efield.text,
                      };
                      http.post(Uri.parse("http://127.0.0.1:5000/signup"),
                      headers: {"Content-Type": "application/json"},
                          body: jsonEncode(someMap)).then((response) async{
                        dynamic resp =json.decode(response.body);
                        print(resp["Error"]);
                        if(resp["Error"]== ""){
                          final box = GetStorage();
                          box.write("public_key", resp["publicKey"]);
                          box.write("private_key", resp["privateKey"]);
                          box.write("username", username.text);
                          box.write("n", resp["n"]);
                          box.write("p", pfield.text);
                          box.write("q", qfield.text);
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => ChatRoom()),
                          );
                        }
                        else{
                          setState(() {
                            errormsg = resp["Error"];
                          });
                        }
                      });
                    },
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
