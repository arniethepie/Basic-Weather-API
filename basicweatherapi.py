from pathlib import Path
import requests, sys, os
# api operations class
class APIoperations(object):
    def __init__(self, candidateNumber, api, filePath):
        self.api = api
        self.candidateNumber = int(candidateNumber)
        self.filePath = filePath
    def get_api_call(self):
        return self.api
    def get_candidateNumber(self):
        return self.candidateNumber
    def get_filePath(self):
        return self.filePath
    
    def set_apiCall(self, newAPI):
        self.api = newAPI
    def set_candidateNumber(self, newCandidateNumber):
        self.candidateNumber = newCandidateNumber
    def set_filePath(self, newFilePath):
        self.filePath = newFilePath

    # returns the api response
    def get_APIResponse(self, city):
        if city == "all":
            query = self.api + "/cities"
            response = requests.get(query)
            return response.json()
        else:
            query = self.api +  "/weather/" + str(self.candidateNumber) + "/" + city 
            response = requests.get(query)
            return response.json()


    # helper methods
    @staticmethod
    def get_apiValidatedResponse(apiCall, returnJSON = True):
        try:
            # check api
            response = requests.get(apiCall)
            response.raise_for_status()
            
            return apiCall
        except Exception:
            raise SystemExit("Please enter a valid API")
    @staticmethod
    def validate_Path(filePath, fileName):
        fullPath = ""
        if filePath == 'current':
            fullPath = str(Path().absolute()) + "/" + fileName
        else:
            if filePath[-1] == "/":
                fullPath = filePath + fileName
            else:
                fullPath = filePath + '/' + fileName


        
        # if file does not exist and in writable
        if os.access(os.path.dirname(fullPath), os.W_OK):
            return fullPath
        else:
            raise SystemExit("Invalid File Path")
    @staticmethod
    def inputCheck(argList):
        try:
            # check candidate
            candidateNumber = int(argList[0])
            apiLink = argList[1]
            filePath = argList[2]
            fileName = argList[3]
            # check api
            validatedAPI = APIoperations.get_apiValidatedResponse(apiLink)
            # check filepath
            validatedPath = APIoperations.validate_Path(filePath, fileName)

            return candidateNumber, validatedAPI, validatedPath
        except IndexError:
            raise SystemExit("Please enter the candidate number, API, file path and file name, separated by a space")
        except ValueError:
            raise SystemExit("Please enter a valid candidate number")


class solutions(object):
    # initialises the specific weather API object for these questions
    def __init__(self, weatherAPIObject):
        self.weatherAPI = weatherAPIObject
    
    def question1(self):
        fullResponse = self.weatherAPI.get_APIResponse("bath")
        answer = (fullResponse["friday"][10])["temperature"]
        return answer

    def question2(self):
        fullResponse = self.weatherAPI.get_APIResponse("edinburgh")
        for hour in fullResponse["friday"]:
            if hour["pressure"] < 1000:
                return True
            return False

    def question3(self):
        fullResponse = self.weatherAPI.get_APIResponse("cardiff")
        everyHour = []
        for day in fullResponse:
            everyHour.extend(fullResponse[day])
        everyHour = sorted(everyHour, key = lambda item: item["temperature"])
        length = len(everyHour)
                
        median = ((everyHour[-1 + length//2])["temperature"] + (everyHour[length//2])["temperature"])/2
        return median

    def question4(self):
        fullResponse = self.weatherAPI.get_APIResponse("all")
        topSpeed = 0
        topCity = ""
        for city in fullResponse["cities"]:
            cityData = self.weatherAPI.get_APIResponse(city)

            for day in cityData:
                for hour in cityData[day]:
                    if hour["wind_speed"] > topSpeed:
                        topSpeed = hour["wind_speed"]
                        topCity = city
                    elif hour["wind_speed"] == topSpeed:
                        if city > topCity:
                            topCity = city
        return topCity

    def question5(self):
        fullResponse = self.weatherAPI.get_APIResponse("all")
        for city in fullResponse["cities"]:
            cityData = self.weatherAPI.get_APIResponse(city)
            for day in cityData:
                for hour in cityData[day]:
                    if hour["temperature"] < 2 and hour["precipitation"] != 0:
                        return True
        return False

    # answers all questions
    def answerAll(self):
        answers = [self.question1(), self.question2(), self.question3(), self.question4(), self.question5()]
        return answers

    def writeFile(self, answers):
        with open(self.weatherAPI.get_filePath() + '.txt', 'w') as f:
            f.write(str(answers))






if __name__ == "__main__":
    candidateNumber, apiLink, filePath = APIoperations.inputCheck(sys.argv[1:])

    weatherAPIObject = APIoperations(candidateNumber, apiLink, filePath)

    answersObject = solutions(weatherAPIObject)
    finalAnswers = answersObject.answerAll()
    answersObject.writeFile(finalAnswers)
    print(finalAnswers)


    