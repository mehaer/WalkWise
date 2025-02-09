import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, Platform } from 'react-native';
import * as Location from 'expo-location';

export default function App() {
  const [alertMessage, setAlertMessage] = useState('');
  const [location, setLocation] = useState({
    coords: {
      latitude: 0,
      longitude: 0,
    },
  });

  const sendAlert = async () => {
    try {
      // Request location permissions
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setAlertMessage('Permission to access location was denied');
        return;
      }

      // Get the current location
      let location = await Location.getCurrentPositionAsync({});
      setLocation(location);

      // Determine the backend URL based on the platform
      const backendUrl =
        Platform.OS === 'ios'
          ? 'http://127.0.0.1:5000/alert' // For iOS simulator
          : Platform.OS === 'android'
          ? 'http://10.0.2.2:5000/alert' // For Android emulator
          : 'http://192.168.x.x:5000/alert'; // Replace with your machine's local IP for physical devices

      // Send the alert to the backend
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: location.coords.latitude,
          longitude: location.coords.longitude,
        }),
      });

      const data = await response.json();
      setAlertMessage(data.message || 'Alert sent successfully!');
    } catch (error) {
      console.error('Error sending alert:', error);
      setAlertMessage('Failed to send alert. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>WalkWise</Text>
      <Button title="Send Alert" onPress={sendAlert} />
      {alertMessage ? <Text>{alertMessage}</Text> : null}
      {location.coords.latitude !== 0 && (
        <>
          {/* <Text>Latitude: {location.coords.latitude}</Text> */}
          {/* <Text>Longitude: {location.coords.longitude}</Text> */}
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
});