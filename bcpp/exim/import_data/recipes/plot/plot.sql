/*
CREATE TABLE `plot_oldplot` (
`plot_identifier` varchar(25) NOT NULL,
`gps_lon` DECIMAL(11,8) DEFAULT NULL,
`gps_lat` DECIMAL(11,8) DEFAULT NULL,
`status` varchar(35) DEFAULT NULL,
`confirmed` varchar(25) DEFAULT NULL,
`selected` varchar(25) DEFAULT NULL,
`community` varchar(25) NOT NULL,
`modified` datetime NOT NULL,
PRIMARY KEY (`plot_identifier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
*/

LOAD DATA INFILE '/Users/erikvw/bcpp_201703/bcpp_household/plot.csv'
INTO TABLE edc_migrated.plot_oldplot
CHARACTER SET utf8
FIELDS TERMINATED BY '|' ENCLOSED BY '"'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES
(plot_identifier,confirmed,status,selected,community,@modified,@gps_lon,@gps_lat)
SET 
modified = NULLIF(STR_TO_DATE(@modified, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
gps_lon = NULLIF(@gps_lon, 0.0),
gps_lat = NULLIF(@gps_lat, 0.0)

UPDATE plot_plot
LEFT JOIN plot_oldplot on plot_plot.plot_identifier=plot_oldplot.plot_identifier
SET
plot_plot.gps_confirmed_longitude=plot_oldplot.gps_lon, 
plot_plot.gps_confirmed_latitude=plot_oldplot.gps_lat
WHERE plot_oldplot.gps_lon IS NOT NULL;

UPDATE plot_plot
LEFT JOIN plot_oldplot on plot_plot.plot_identifier=plot_oldplot.plot_identifier
SET
plot_plot.selected=plot_oldplot.selected 
WHERE plot_oldplot.selected IS NOT NULL;

update plot_plot set selected = NULL where selected='';


update plot_plot 
inner join (select distinct plot_identifier from bcpp_subject_subjectconsent as sc
left join member_householdmember as hhm on sc.household_member_id=hhm.id
left join household_householdstructure as hhs on hhm.household_structure_id=hhs.id
left join household_household as hh on hhs.household_id=hh.id
left join plot_plot as p on hh.plot_id=p.id) as A on A.plot_identifier=plot_plot.plot_identifier
set plot_plot.enrolled=True;


/*
CREATE TABLE `plot_oldplot2` (
`plot_identifier` varchar(25) NOT NULL,
`comment` varchar(250) DEFAULT NULL,
`description` varchar(250) DEFAULT NULL,
PRIMARY KEY (`plot_identifier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
*/

LOAD DATA INFILE '/Users/erikvw/bcpp_201703/bcpp_household/plot2.csv'
INTO TABLE edc_migrated.plot_oldplot2
CHARACTER SET utf8
FIELDS TERMINATED BY '|' ENCLOSED BY '"'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES
(plot_identifier,@description,@comment)
SET
description=SUBSTRING(@description,1,250),
comment=SUBSTRING(@comment,1,250);


UPDATE plot_plot
LEFT JOIN plot_oldplot2 on plot_plot.plot_identifier=plot_oldplot2.plot_identifier
SET
plot_plot.comment=plot_oldplot2.comment, 
plot_plot.description=plot_oldplot2.description;
