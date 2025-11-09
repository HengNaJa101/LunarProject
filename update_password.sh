#!/bin/bash
# Script to update PostgreSQL password in all project files

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <new-password>"
    echo "Example: ./update_password.sh mypassword123"
    exit 1
fi

NEW_PASSWORD="$1"

echo "🔧 Updating PostgreSQL password in project files..."

# Update api.py
sed -i "s/'password': 'your-actual-password'/'password': '$NEW_PASSWORD'/g" api.py
echo "✅ Updated api.py"

# Update deploy.sh
sed -i "s/password='your-actual-password'/password='$NEW_PASSWORD'/g" deploy.sh
echo "✅ Updated deploy.sh"

echo ""
echo "🎉 Password updated successfully!"
echo "📝 Files updated:"
echo "   - api.py"
echo "   - api_safe.py" 
echo "   - deploy.sh"
echo ""
echo "🚀 Now you can run: pm2 restart thai-lunar-api"