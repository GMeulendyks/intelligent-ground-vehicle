#include <fstream>
#include <iostream>
#include <string>
#include <chrono>

using namespace std;
using namespace std::chrono;

string readCSVLine(const string& filename) {
    ifstream file(filename);
    string line;
    
    if (!file.is_open()) {
        cerr << "Error: File could not be opened." << endl;
        return "";  // Return empty string if the file cannot be opened
    }
    
    if (getline(file, line)) {
        // Successfully read a line
        file.close();
        return line;
    } else {
        // No line read, possibly an empty file or end of file reached
        file.close();
        return "";
    }
}

void appendCSVLine(const string& filename, const string& line) {
    ofstream file(filename, ios::app);  // Open file in append mode

    if (!file.is_open()) {
        cerr << "Error: File could not be opened." << endl;
        return;  // Exit the function if the file cannot be opened
    }

    file << line << endl;  // Append the line with a newline at the end
    file.close();  // Close the file after appending
}

int main(void) {
    string filename = "training_data.csv"; // Specify the filename
    string firstLine = readCSVLine(filename);
    auto start = high_resolution_clock::now();
    appendCSVLine(filename, firstLine);
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start).count();
    double seconds = static_cast<double>(duration) * 0.000001;
    cout << "Time taken to append line: " << seconds << " seconds." << endl;
    // cout << "First line of the file: " << firstLine << endl;
    return 0;
}
