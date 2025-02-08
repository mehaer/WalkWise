import React, { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function App() {
  const [status, setStatus] = useState('Monitoring');

  const activateWalkWise = () => {
    setStatus('Active - Listening & Monitoring');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>WalkWise</Text>
      <Text>Status: {status}</Text>
      <Button title="Activate WalkWise" onPress={activateWalkWise} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
});
