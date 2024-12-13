import 'package:flutter/material.dart';
import 'admin_home.dart';
import 'admin_route.dart';
import 'admin_profile.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Eco Mitra',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false,
      home: const admin_navigation(),
    );
  }
}

class admin_navigation extends StatefulWidget {
  const admin_navigation({super.key});

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<admin_navigation> {
  final List<String> _titles = [
    "Admin Dashboard",
    "Route",
    "Profile",
  ];

  final List<Widget> _screens = [
    const admin_home(),
    const admin_route(),
    const admin_profile(),

  ];

  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            _titles[_selectedIndex],
            style: const TextStyle(color: Colors.white),
          ),
        ),
        backgroundColor: const Color(0xFF00BF63), // Green background for AppBar
      ),
      body: Center(
        child: _screens[_selectedIndex],
      ),
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          labelTextStyle: WidgetStateProperty.all(
            const TextStyle(color: Colors.white), // Unselected label color
          ),
          indicatorColor: Colors.white38, // Optional: Remove the indicator
        ),
        child: NavigationBar(
          height: 80,
          backgroundColor: const Color(0xFF00BF63),
          selectedIndex: _selectedIndex,
          onDestinationSelected: _onItemTapped,
          destinations: [
            NavigationDestination(
              icon: const Icon(Icons.home, color: Colors.white),
              label: 'Home',
            ),
            NavigationDestination(
              icon: const Icon(Icons.route, color: Colors.white),
              label: 'Route',
            ),
            NavigationDestination(
              icon: const Icon(Icons.person, color: Colors.white),
              label: 'Profile',
            ),
          ],
        ),
      ),
    );
  }
}


