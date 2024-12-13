import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class admin_home extends StatefulWidget {
  const admin_home({super.key});

  @override
  State<admin_home> createState() => _admin_homeState();
}

class _admin_homeState extends State<admin_home> {
  @override
  Widget build(BuildContext context) {
    return  Scaffold(
      body:
          Center(
            child:
            Column(
              children: [
                Transform.translate(offset: Offset(0, 20),
                  child: Text("Routes", 
                    style: TextStyle(fontSize: 20, color: Colors.black, fontWeight: FontWeight.bold),
                )
                ),
                Column(
                  children: [
                    Transform.translate(offset: Offset(0, 40),
                      child: Column(
                        children: [
                          ElevatedButton(onPressed: (){
                            print("Button Clicked");
                          }, child: Text("Kalimati", style: TextStyle(color: Colors.white, fontSize: 18),),
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Color(0xFF00BF63),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10),
                                ),
                              fixedSize: Size(160,50),
                            ),

                          ),
                          SizedBox(height: 10),
                          ElevatedButton(onPressed: (){
                            print("Button Clicked");
                          }, child: Text("Baneshowr", style: TextStyle(color: Colors.white, fontSize: 18),),
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Color(0xFF00BF63),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10),
                                ),
                              fixedSize: Size(160,50),
                            ),

                          ),
                          SizedBox(height: 10),
                          ElevatedButton(onPressed: (){
                            print("Button Clicked");
                          }, child: Text("Kadaghari", style: TextStyle(color: Colors.white, fontSize: 18),),
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Color(0xFF00BF63),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10),
                                ),
                              fixedSize: Size(160,50),
                            ),
                          )
                        ],
                      ),
                    )
                  ],
                )
              ],
            ),
          )
      
      
      // Column(
      //   children: [
      //     ElevatedButton(onPressed: (){
      //       print("Button Pressed");
      //     },
      //
      //   child: Text("Kalimati"))
      //   ],
      // ),
    );
  }
}
