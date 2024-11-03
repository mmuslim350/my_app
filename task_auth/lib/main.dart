import 'package:flutter/material.dart';
import 'package:task_auth/pages/login_page.dart';
import 'package:task_auth/pages/register_page.dart';
import 'package:task_auth/pages/verify_code.dart';

void main() => runApp(const MyHome());

class MyHome extends StatelessWidget {
  const MyHome({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My_App',
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterPage(),
        '/home': (context) => const HomePage(),
        '/verify_otp': (context) => const VerifyOtpPage(),
      },
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('HOME PAGE'),
        centerTitle: true,
      ),
      body: SafeArea(
          child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
            child: ElevatedButton(
              onPressed: () {
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/login',
                  ModalRoute.withName('/login'),
                );
              },
              child: Text('LOGOUT'),
            ),
          ),
        ],
      )),
    );
  }
}
