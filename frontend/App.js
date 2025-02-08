import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, Alert } from 'react-native';

export default function App() {
  const [status, setStatus] = useState('Monitoring');
  const [alertMessage, setAlertMessage] = useState('');

  const activateWalkWise = () => {
    setStatus('Active - Listening & Monitoring');
  };

  const sendAlert = async () => {
    try {
      console.log('Sending alert...');
      const response = await fetch('http://127.0.0.1:5000/alert', {
        method: 'GET',
      });
      const data = await response.json();
      console.log('Response:', data);
      setAlertMessage(data.message);
      Alert.alert('Alert', data.message);
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'Failed to send alert');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>WalkWise</Text>
      <Text>Status: {status}</Text>
      <Button title="Activate WalkWise" onPress={activateWalkWise} />
      <Button title="Send Alert" onPress={sendAlert} />
      {alertMessage ? <Text style={styles.alertMessage}>{alertMessage}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
  alertMessage: { marginTop: 20, fontSize: 18, color: 'red' },
});