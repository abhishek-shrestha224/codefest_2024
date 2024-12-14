class User {
  final String role;

  User({required this.role});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(role: json['role']);
  }
}

class LoginResponse {
  final String accessToken;
  final String refreshToken;
  final User user;

  LoginResponse({
    required this.accessToken,
    required this.refreshToken,
    required this.user,
  });
  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      accessToken: json['access_token'],
      refreshToken: json['refresh_token'],
      user: User.fromJson(json['user']),
    );
  }
}

class RefreshResponse {
  final String accessToken;

  RefreshResponse({
    required this.accessToken,
  });
  factory RefreshResponse.fromJson(Map<String, String> json) {
    return RefreshResponse(
      accessToken: json['access_token'],
    );
  }
}


class TripResponse {
  final bool active;
  final TripData? tripData;

  TripResponse({required this.active, this.tripData});

  // Factory constructor to create a TripResponse instance from JSON
  factory TripResponse.fromJson(Map<String, dynamic> json) {
    return TripResponse(
      active: json['active'],
      tripData: json['trip_data'] != null
          ? TripData.fromJson(json['trip_data'])
          : null,
    );
  }

  // Method to convert a TripResponse instance to JSON
  Map<String, dynamic> toJson() {
    return {
      'active': active,
      'trip_data': tripData?.toJson(),
    };
  }
}

class TripData {
  final Trip trip;
  final List<Location> locations;

  TripData({required this.trip, required this.locations});

  // Factory constructor to create a TripData instance from JSON
  factory TripData.fromJson(Map<String, dynamic> json) {
    return TripData(
      trip: Trip.fromJson(json['trip']),
      locations: (json['locations'] as List)
          .map((locationJson) => Location.fromJson(locationJson))
          .toList(),
    );
  }

  // Method to convert a TripData instance to JSON
  Map<String, dynamic> toJson() {
    return {
      'trip': trip.toJson(),
      'locations': locations.map((location) => location.toJson()).toList(),
    };
  }
}
