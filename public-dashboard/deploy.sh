#!/bin/bash

echo "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
echo "  ULTRON DASHBOARD QUICK DEPLOY  "
echo "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
echo ""
echo "Choose your deployment platform:"
echo ""
echo "1) 🌐 Netlify (drag & drop)"
echo "2) ▲ Vercel"
echo "3) 📄 GitHub Pages"
echo "4) ⚡ Surge.sh (requires npm)"
echo "5) 🔧 Local server"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🌐 NETLIFY DEPLOYMENT:"
        echo "1. Visit: https://app.netlify.com/drop"
        echo "2. Drag the 'public-dashboard' folder to the page"
        echo "3. Get your live URL instantly!"
        echo ""
        echo "📁 Files ready in: $(pwd)/public-dashboard/"
        ;;
    2)
        echo ""
        echo "▲ VERCEL DEPLOYMENT:"
        echo "1. Visit: https://vercel.com"
        echo "2. Click 'New Project'"
        echo "3. Upload the 'public-dashboard' folder"
        echo "4. Deploy and get your URL!"
        echo ""
        echo "📁 Files ready in: $(pwd)/public-dashboard/"
        ;;
    3)
        echo ""
        echo "📄 GITHUB PAGES DEPLOYMENT:"
        echo "1. Create a new GitHub repository"
        echo "2. Upload the index.html file"
        echo "3. Go to Settings > Pages"
        echo "4. Enable GitHub Pages"
        echo "5. Access your dashboard!"
        echo ""
        echo "📁 Files ready in: $(pwd)/public-dashboard/"
        ;;
    4)
        echo ""
        echo "⚡ SURGE.SH DEPLOYMENT:"
        if command -v npm &> /dev/null; then
            echo "Installing Surge..."
            npm install -g surge
            echo ""
            echo "Deploying to Surge..."
            cd public-dashboard
            surge
        else
            echo "❌ NPM not found. Please install Node.js first:"
            echo "   Visit: https://nodejs.org"
            echo ""
            echo "Then run: npm install -g surge"
            echo "         cd public-dashboard"
            echo "         surge"
        fi
        ;;
    5)
        echo ""
        echo "🔧 STARTING LOCAL SERVER..."
        echo ""
        cd public-dashboard
        echo "🚀 Dashboard will be available at: http://localhost:8000"
        echo "📊 Press Ctrl+C to stop the server"
        echo ""
        if command -v python3 &> /dev/null; then
            python3 -m http.server 8000
        elif command -v python &> /dev/null; then
            python -m http.server 8000
        else
            echo "❌ Python not found. Please install Python first."
            echo "   Alternative: Use any static file server"
        fi
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        ;;
esac

echo ""
echo "🌟 Your ULTRON Agent Dashboard is ready!"
echo "   All files are in: $(pwd)/public-dashboard/"