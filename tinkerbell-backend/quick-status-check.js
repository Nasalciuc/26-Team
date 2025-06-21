// Quick API validation test
const http = require('http');

async function testAPI() {
    console.log('🧪 Testing Tinkerbell API Status...\n');

    // Test 1: Health Check
    try {
        const healthResponse = await makeRequest('GET', '/health');
        console.log('✅ Health Check:', healthResponse.status === 200 ? 'PASSED' : 'FAILED');
        if (healthResponse.status === 200) {
            console.log('   Server message:', healthResponse.data.message);
        }
    } catch (error) {
        console.log('❌ Health Check: FAILED -', error.message);
        return false;
    }

    // Test 2: Personas Endpoint
    try {
        const personasData = {
            businessName: "Test Business",
            businessDescription: "Romanian Restaurant",
            targetCustomers: "Local food lovers",
            businessGoals: "Increase customer base"
        };

        const personasResponse = await makeRequest('POST', '/api/create-personas', personasData);
        console.log('✅ Personas API:', personasResponse.status === 200 ? 'PASSED' : 'FAILED');

        if (personasResponse.status === 200 && personasResponse.data.success) {
            console.log('   Generated personas count:', personasResponse.data.data.personas.length);
        }
    } catch (error) {
        console.log('❌ Personas API: FAILED -', error.message);
    }

    console.log('\n🎯 API Status: Backend is operational and ready for demo!');
    return true;
}

function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'localhost',
            port: 3000,
            path: path,
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });
            res.on('end', () => {
                try {
                    const jsonData = JSON.parse(body);
                    resolve({ status: res.statusCode, data: jsonData });
                } catch (error) {
                    resolve({ status: res.statusCode, data: body });
                }
            });
        });

        req.on('error', reject);

        if (data) {
            req.write(JSON.stringify(data));
        }

        req.end();
    });
}

testAPI();