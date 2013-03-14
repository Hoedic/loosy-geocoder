from googlegeocoder import GoogleGeocoder
import csv

geocoder = GoogleGeocoder()
import time

exclusion = "Montreal, QC, Canada" 

def geocodeMe (geocode_string, mode):

    #print "Will geocode mode: %s for string %s" % (mode, geocode_string)
    search_output = geocoder.get(geocode_string)

    if(len(search_output) == 0):
        #print "/////Empty - worst case scenario"
        return []
    if(len(search_output) == 1 and len(search_output[0].types) > 0 and search_output[0].types[0] == mode):
        #print "/////Best case scenario"
        return [str(search_output[0].geometry.location.lat), str(search_output[0].geometry.location.lng), str(len(search_output)), "OK", search_output[0].formatted_address]

    elif (len(search_output) == 1):
        #print "/////Second best case scenario"
        return [str(search_output[0].geometry.location.lat), str(search_output[0].geometry.location.lng), str(len(search_output)), "KO", search_output[0].formatted_address]

    else:
        #print "/////Well... worse case scenario"
        match_list = []
        for result in search_output:
            #print "J'ai un result : %s " % (result)
            #print result.types[0]
            if (len(result.types) > 0 and  result.types[0] == mode):
               match_list.extend([str(result.geometry.location.lat), str(result.geometry.location.lng), result.formatted_address])
               #print "match list lengh: %s" % (len(match_list))
        if(len(match_list) > 0):
            temp_list = [str(match_list[0]), str(match_list[1]), str(len(search_output)), "KO", match_list[2]]
        else: 
            temp_list = [str(search_output[0].geometry.location.lat), str(search_output[0].geometry.location.lng), str(len(search_output)), "KO", search_output[0].formatted_address]
        temp_list.extend(match_list)
        return temp_list 
                

    #for place in search:
    #    print place.__dict__
    #    print place.geometry.location.lat

    return(search[0].geometry.location.lat, search[0].geometry.location.lng, len(search))

test_file = 'accident.2011.full.uniq.3517.in'
csv_file = csv.DictReader(open(test_file, 'rU'), delimiter=';', quotechar='"')

#print csv_file
print ";".join(csv_file.fieldnames) + ";lat;lng;nb results;status;formatted address"

for ligne in csv_file:
    time.sleep(.5)
    if (ligne and len(ligne['Geocoder']) > 0) : 
        #print "Sur le point d'appeler le geocoder pour '%s'\n" % ligne['Geocoder']
        result_list = geocodeMe(ligne['Geocoder'], ligne['Mode'])
        #print result_list

        if (len(result_list) > 4 and  result_list[4] == exclusion ):
            #print "exclusion list!"
            result_list[0] = "0.000"
            result_list[1] = "0.000"
            result_list[3] = "KO"

        string = ";".join(ligne.values()) + ";" 
        string += ";".join(result_list)
        print string 


