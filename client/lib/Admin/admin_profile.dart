import 'package:flutter/material.dart';

class admin_profile extends StatefulWidget {
  const admin_profile({super.key});

  @override
  State<admin_profile> createState() => _LoginState();
}

class _LoginState extends State<admin_profile> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 25),

              Center(
                child: Image.asset(
                  'Assets/Icons/user.png',
                  height: 80,
                  width: 80,
                ),
              ),

              SizedBox(height: 10),

              // Login Title and Subtitle
              Center(
                child:
                Text(
                  "Rashug Gautam",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 16),

              // Email Input
              Padding(padding: EdgeInsets.only(left: 8),
                child:
                Text(
                  "Admin Id",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 5),
              Padding(
                padding: EdgeInsets.only(left: 8, right: 10),
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(40),
                    ),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  ),
                  controller: TextEditingController(
                    text: "Id-223142", // Set the default text here.
                  ),
                  enabled: false, // Disable the TextField.
                ),
              ),

              SizedBox(height: 16),

              // Email Input
              Padding(padding: EdgeInsets.only(left: 8),
                child:
                Text(
                  "First Name",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 5),
              Padding(
                padding: EdgeInsets.only(left: 8, right: 10),
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(40),
                    ),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  ),
                  controller: TextEditingController(
                    text: "Rashug", // Set the default text here.
                  ),
                  enabled: false, // Disable the TextField.
                ),
              ),

              SizedBox(height: 16),

              // Email Input
              Padding(padding: EdgeInsets.only(left: 8),
                child:
                Text(
                  "Last Name",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 5),
              Padding(
                padding: EdgeInsets.only(left: 8, right: 10),
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(40),
                    ),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  ),
                  controller: TextEditingController(
                    text: "Gautam", // Set the default text here.
                  ),
                  enabled: false, // Disable the TextField.
                ),
              ),

              SizedBox(height: 16),

              // Email Input
              Padding(padding: EdgeInsets.only(left: 8),
                child:
                Text(
                  "Email",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 5),
              Padding(
                padding: EdgeInsets.only(left: 8, right: 10),
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(40),
                    ),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  ),
                  controller: TextEditingController(
                    text: "rashug@gmail.com", // Set the default text here.
                  ),
                  enabled: false, // Disable the TextField.
                ),
              ),

              SizedBox(height: 16),

              // Email Input
              Padding(padding: EdgeInsets.only(left: 8),
                child:
                Text(
                  "Address",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 5),
              Padding(
                padding: EdgeInsets.only(left: 8, right: 10),
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(40),
                    ),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  ),
                  controller: TextEditingController(
                    text: "Sankhamul, Baneshowr", // Set the default text here.
                  ),
                  enabled: false, // Disable the TextField.
                ),
              ),

              SizedBox(height: 16),

              // Email Input
              Padding(padding: EdgeInsets.only(left: 8),
                child:
                Text(
                  "Role",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ),

              SizedBox(height: 5),
              Padding(
                padding: EdgeInsets.only(left: 8, right: 10),
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(40),
                    ),
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  ),
                  controller: TextEditingController(
                    text: "Admin", // Set the default text here.
                  ),
                  enabled: false, // Disable the TextField.
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
