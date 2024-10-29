SELECT 
    hotel_id,
    night_of_stay AS day,
    COUNT(CASE WHEN rpg_status = 1 THEN 1 END) AS daily_bookings,
    COUNT(CASE WHEN rpg_status = 2 THEN 1 END) AS daily_cancellations,
    COUNT(DISTINCT room_id) AS rooms_occupied, 
    COUNT(DISTINCT room_id) * 100.0 / (SELECT COUNT(*) FROM base_event WHERE hotel_id = b.hotel_id) AS occupancy_rate
FROM
    base_event b
WHERE hotel_id = 2607
GROUP BY 
    hotel_id, night_of_stay
ORDER BY 
    night_of_stay;
