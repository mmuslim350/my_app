import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class VerifyOtpPage extends StatefulWidget {
  const VerifyOtpPage({super.key});

  @override
  State<VerifyOtpPage> createState() => _VerifyOtpPageState();
}

class _VerifyOtpPageState extends State<VerifyOtpPage> {
  final TextEditingController _otpController = TextEditingController();

  Future<void> _verifyOtp() async {
    if (_otpController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('OTP tidak boleh kosong')),
      );
      return;
    }

    final response = await http.post(
      Uri.parse(
          'http://localhost:5000/verify_otp'), // Use this for Android emulator
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {
        'otp': _otpController.text, // Pass only the OTP
      },
    );
    Navigator.pushReplacementNamed(context, '/login');
    // final Map<String, dynamic> responseData = json.decode(response.body);

    // if (response.statusCode == 200 && responseData['status'] == 'success') {
    //   Navigator.pushReplacement(
    //       context, MaterialPageRoute(builder: (context) => const HomePage()));
    // } else {
    //   // Show error message if verification fails
    //   ScaffoldMessenger.of(context).showSnackBar(
    //     SnackBar(content: Text(responseData['message'])),
    //   );
    // }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Verify OTP'),
        centerTitle: true,
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextFormField(
              controller: _otpController,
              decoration: const InputDecoration(
                labelText: 'Enter OTP',
                border: OutlineInputBorder(),
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'OTP tidak boleh kosong';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _verifyOtp,
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: const Text(
                'Verify OTP',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
