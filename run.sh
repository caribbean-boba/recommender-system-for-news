brew services start redis
brew services start mongodb
cd backend
python service.py &

cd ../frontend/servers
npm start &

cd ../recommender-system-service
python recommender_system.py &
python log_processor.py

cd ../news-modeling-and-training
python model_server.py &

# cd ../helpers
# ./run.sh

echo "************************************"
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY
echo "************************************"

kill $(jobs -p)