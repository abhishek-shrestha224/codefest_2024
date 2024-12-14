
class Trip {
  final int id;
  final bool active;
  final DateTime updatedAt;
  final String name;
  final DateTime createdAt;

  Trip({
    required this.id,
    required this.active,
    required this.updatedAt,
    required this.name,
    required this.createdAt,
  });

  factory Trip.fromJson(Map<String, dynamic> json) {
    return Trip(
      id: json['id'],
      active: json['active'],
      updatedAt: DateTime.parse(json['updated_at']),
      name: json['name'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'active': active,
      'updated_at': updatedAt.toIso8601String(),
      'name': name,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

class Location {
  final double radiusKm;
  final int id;
  final double lon;
  final double lat;
  final String name;

  Location({
    required this.radiusKm,
    required this.id,
    required this.lon,
    required this.lat,
    required this.name,
  });

  // Factory constructor to create a Location instance from JSON
  factory Location.fromJson(Map<String, dynamic> json) {
    return Location(
      radiusKm: json['radius_km'],
      id: json['id'],
      lon: json['lon'],
      lat: json['lat'],
      name: json['name'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'radius_km': radiusKm,
      'id': id,
      'lon': lon,
      'lat': lat,
      'name': name,
    };
  }
}

class User {
  final String lastName;
  final String firstName;
  final String address;
  final DateTime createdAt;
  final String email;
  final int locationId;
  final String role;
  final int id;
  final DateTime updatedAt;

  User({
    required this.lastName,
    required this.firstName,
    required this.address,
    required this.createdAt,
    required this.email,
    required this.locationId,
    required this.role,
    required this.id,
    required this.updatedAt,
  });

  // Factory constructor to create a User instance from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      lastName: json['last_name'],
      firstName: json['first_name'],
      address: json['address'],
      createdAt: DateTime.parse(json['created_at']),
      email: json['email'],
      locationId: json['location_id'],
      role: json['role'],
      id: json['id'],
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  // Method to convert a User instance to JSON
  Map<String, dynamic> toJson() {
    return {
      'last_name': lastName,
      'first_name': firstName,
      'address': address,
      'created_at': createdAt.toIso8601String(),
      'email': email,
      'location_id': locationId,
      'role': role,
      'id': id,
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}
