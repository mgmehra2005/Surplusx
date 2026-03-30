const donorListElement = document.getElementById('donor-list');
const donorListStatusElement = document.getElementById('donor-list-status');
const featureStatusElement = document.getElementById('feature-status');
const refreshDonorsButton = document.getElementById('refresh-donors-btn');
const profileButton = document.getElementById('profile-btn');
const loginButton = document.getElementById('login-btn');
const logoutButton = document.getElementById('logout-btn');
const historyButton = document.getElementById('history-btn');

async function loadDonors() {
    donorListStatusElement.textContent = 'Loading donors...';
    donorListElement.innerHTML = '';

    try {
        const response = await fetch('/api/food/donor-list');
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        const donors = Array.isArray(data)
            ? data
            : Array.isArray(data.donors)
                ? data.donors
                : [];

        if (!donors.length) {
            donorListStatusElement.textContent = 'No donors found.';
            return;
        }

        donors.forEach((donor) => {
            const item = document.createElement('li');
            if (typeof donor === 'string') {
                item.textContent = donor;
            } else {
                const donorName = donor.name || donor.username || 'Unnamed donor';
                const donorLocation = donor.location ? ` - ${donor.location}` : '';
                item.textContent = `${donorName}${donorLocation}`;
            }
            donorListElement.appendChild(item);
        });

        donorListStatusElement.textContent = `Loaded ${donors.length} donor(s).`;
    } catch (error) {
        if (error && typeof error.message === 'string' && error.message.includes('status 5')) {
            donorListStatusElement.textContent = 'Server error occurred while loading donors.';
        } else {
            donorListStatusElement.textContent = 'Unable to connect to donor list service.';
        }
    }
}

function showFeatureUnavailable(featureName) {
    featureStatusElement.textContent = `${featureName} API is not available yet.`;
}

refreshDonorsButton.addEventListener('click', loadDonors);
// Profile/Login/Logout/History API endpoints are not available in backend yet.
profileButton.addEventListener('click', () => showFeatureUnavailable('Profile'));
loginButton.addEventListener('click', () => showFeatureUnavailable('Login'));
logoutButton.addEventListener('click', () => showFeatureUnavailable('Logout'));
historyButton.addEventListener('click', () => showFeatureUnavailable('Donor History'));

loadDonors();
