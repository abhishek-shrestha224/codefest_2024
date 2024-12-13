import 'package:flutter/material.dart';

void main() {
  runApp(const admin_route());
}

class admin_route extends StatelessWidget {
  const admin_route({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Bus Schedule App',
      home: const BusScheduleScreen(),
    );
  }
}

class BusScheduleScreen extends StatelessWidget {
  const BusScheduleScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.grey[200],
        title: const Text(
          "Kalimati Route Distribution",
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        iconTheme: const IconThemeData(color: Colors.black),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            buildBusScheduleCard("Environment management department", "3 mins", "completed"),
            const SizedBox(height: 8),
            buildBusScheduleCard("Kalimati Chowk", "5 mins", "in_transit"),
            const SizedBox(height: 8),
            buildBusScheduleCard("Jana Prabhat School", "7 mins", "pending"),
            const SizedBox(height: 8),
            buildBusScheduleCard("Bafal Chowk", "9 mins", "pending"),
            const SizedBox(height: 8),
            buildBusScheduleCard("Chauni Chowk", "10 mins", "pending"),
            const SizedBox(height: 8),
            buildBusScheduleCard("Chauni Museum", "13 mins", "pending"),
            const SizedBox(height: 8),
            buildBusScheduleCard("Mahendra Ratna Campus", "13 mins", "pending"),
          ],
        ),
      ),
    );
  }

  // Function to manually set the status for each bus schedule card
  Widget buildBusScheduleCard(String route, String time, String status) {
    IconData icon;
    Color iconColor;
    Color timeColor;

    // Set icon and colors based on status
    if (status == 'completed') {
      icon = Icons.check_circle;
      iconColor = Colors.green;
      timeColor = Colors.green;
    } else if (status == 'in_transit') {
      icon = Icons.local_shipping;
      iconColor = Colors.blue;
      timeColor = Colors.blue;
    } else {
      // Default status is 'pending'
      icon = Icons.access_time;
      iconColor = Colors.orange;
      timeColor = Colors.orange;
    }

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.shade300,
            blurRadius: 5,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: ListTile(
        leading: Icon(
          icon,
          color: iconColor,
          size: 28,
        ),
        title: Text(
          route,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Text(
          "Departing in $time",
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              time,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: timeColor,
              ),
            ),
            Icon(
              Icons.access_time,
              color: Colors.grey[600],
              size: 20,
            ),
          ],
        ),
      ),
    );
  }
}
