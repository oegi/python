SELECT DISTINCT (FORMAT(DATEADD(mi, 15, max_datetime), 'dd-MM-yyyy HH:mm', 'es-CL')) AS [last_date],
                [sockets].[ID_SOC],
                [sockets].[IDSOCKET],
                [sockets].[NOINS]
FROM [sockets]
       LEFT OUTER JOIN [socket_channel] ON ([sockets].[ID_SOC] = [socket_channel].[id_soc])
WHERE ([sockets].[DESCRIPTION] = 'Real' AND
       [sockets].[idclient] = 'AASA ENERGIA' AND [sockets].[idclient] IS NOT NULL AND NOT ([sockets].[IDSOCKET] =))
ORDER BY [sockets].[NOINS] ASC


SELECT *
FROM measure_detail
WHERE id_soc = 6448
  and datetime = '2018-12-19 15:00'


SELECT
    CAST(CAST((15 * 6) AS int) / 60 AS varchar) + ':' + right('0' + CAST(CAST((15 * 6) AS int) % 60 AS varchar(2)), 2)
SELECT DATEADD(minute, -(15 * 4), '2018-12-19 15:00');


SELECT *
FROM measure_detail
WHERE id_soc = 6448
  AND datetime between DATEADD(minute, -(15 * 1), '2018-12-19 15:00') and '2018-12-19 15:00'
ORDER BY  datetime ASC