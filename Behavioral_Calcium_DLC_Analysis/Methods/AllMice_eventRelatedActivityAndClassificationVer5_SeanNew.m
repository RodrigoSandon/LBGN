%This code calculates the evoked calcium event rates and fluorescence for
%an arbitrary set of behavioral event timestamps. The responses are
%classified as activated or inhibited based versus a time shuffled null
%distribution of responses to the same event. Firing rate responses can be
%classified (Jimenez et al., 2018) or evoked fluorescent responses can be
%classified.

%coded by Jesse Wood 03/19/18
%% user selected variables
uv.chooseFluoresenceOrRate = 1;                                             %set to 1 to classify fluoresence response; set to 2 to classify firing rate responses
uv.sigma = 1;                                                               %this parameter controls the number of standard deviations that the response must exceed to be classified as a responder. try 1 as a starting value and increase or decrease as necessary.
uv.evtWin = [-10 10];                                                       %time window around each event in sec relative to event times (use long windows here to see more data)
uv.evtSigWin.groomingStart = [-.5 3];                                       %period within time window that response is classified on (sec relative to event)
uv.evtSigWin.groomingStop = [-.5 3];
% uv.evtSigWin.faceGroomingStart = [-.5 2];
% uv.evtSigWin.faceGroomingStop = [-.5 2];
uv.dt = 0.1;                                                                %time step size (sec)
uv.resamples = 1000                                                         %number of resamples to use in shuffle analysis
%% do NOT modify below this line
%% get a list of behavioral events

for i = 1:length(processed)
    behav = processed(i).behav;
    ca = processed(i).ca;
    
    
    evts = fieldnames(behav);                                                   %get each behavioral event name
    %% calculate time windows for each event
    evtWinSpan = max(uv.evtWin) - min(uv.evtWin);                               %calculate length of each period to examine neural activity in
    numMeasurements = evtWinSpan/uv.dt;                                         %calculate the number of measurements in each time window
    time = uv.evtWin(1,1):uv.dt:uv.evtWin(1,2)-uv.dt;                           %the time window around each event
    for e = 1:size(evts,1)                                                      %for each event
        evtWinIdx.(evts{e}) = time >= uv.evtSigWin.(evts{e})(1,1) &...          %calculate logical index for each event period
            time <= uv.evtSigWin.(evts{e})(1,2);
    end
    clear evtWinSpan e
    %%
    tic
    for u = 1:size(ca.events,1)                                                 %for each unit
        unitTS = ca.eventTS{u};                                                 %direct transfer of calcium event timestamps
        unitTrace = ca.traces(u,:);                                             %direct transfer of calcium trace for selected cell
        unitAverage = ca.traceAverage(u,:);                                     %Sean added direct transfer of entire unit average
        unitSD = ca.traceSD(u,:);                                               %Sean added direct transfer of entire unit SD
        %%
        for e = 1:size(evts,1)                                                  %for each behavioral event
            eTS = behav.(evts{e});                                              %direct transfer of behavioral timestamps
            %% initialize trial matrices
            caEvtCtTrials = NaN(size(eTS,1),numMeasurements);                   %initialize trial x time calcium event count matrix
            caTraceTrials = NaN(size(eTS,1),numMeasurements);                   %initialize trial x time calcium trace matrix
            %%
            for t = 1:(size(eTS,1))                                             %for each trial
                %% set each trial's temporal boundaries
                timeWin = [eTS(t)+uv.evtWin(1,1):uv.dt:eTS(t)+uv.evtWin(1,2)];  %calculate time window around each event
                if min(timeWin) > min(ca.time) & max(timeWin) < max(ca.time)    %if the beginning and end of the time window around the event occurred during the recording period. if not, the time window is out of range
                    %% get unit event counts in trials
                    caEvtCtTrials(t,:) = histcounts(unitTS,timeWin);            %histogram counts of ca event times within each time bin
                    %% get unit ca traces in trials
                    idx = ca.time > min(timeWin) & ca.time < max(timeWin);      %logical index of time window around each behavioral event time
                    %caTraceTrials(t,1:sum(idx)) = unitTrace(idx);               %store the evoked calcium trace around each event   (see below, comment out if dont want normalized to whole trace)
                    caTraceTrials(t,1:sum(idx)) = (unitTrace(idx) - unitAverage)/(unitSD); %Sean added normalize evoked trace to cell average before shuffling for each trial
                end
            end
            clear t timeWin idx eTS
            %% convert counts to rate
            caEvtRateTrials = caEvtCtTrials/uv.dt;                              %calcium event rate equals the calcium event count divided by the duration of the time bin
            %% shuffle and resample the data
            trialCt = size(caTraceTrials,1);                                    %number of trials for currently analyzed event
            for g = 1:uv.resamples                                              %for each resampling of the data
                [~,shuffledIDX] = sort(randi...                                 %generate a matrix of random integers from 1 to the number of measurements in each time window (not each number is generated/some are repeated)
                    (numMeasurements,trialCt,numMeasurements),2);               %sort the data index to create a new list of indices
                for t = 1:trialCt                                               %for each trial
                    shuffledTrace(t,:) = caTraceTrials(t,shuffledIDX(t,:));     %shuffle the calcium trace
                    shuffledEvtRate(t,:) = caEvtRateTrials(t,shuffledIDX(t,:)); %shuffle the event rate
                end
                nullDistTrace(g,:) = nanmean(shuffledTrace);                    %calculate the NaN mean of the shuffled traces
                nullDistEvtRate(g,:) = nanmean(shuffledEvtRate);                %calculate the NaN mean of the shuffled event rates
            end
            clear shuffled* g t trialCt
            %% choose to classify fluoresence or event rates
            if uv.chooseFluoresenceOrRate == 1                                  %if user selected to classify the fluoresence
                nullDist = nullDistTrace;                                       %direct transfer
                empiricalTrialWin = nanmean...
                    (caTraceTrials(:,evtWinIdx.(evts{e})),2);                   %NaN mean of the fluorescent response across trials, within the time window. this gets the within trial mean.
                empiricalWinAvg = nanmean(empiricalTrialWin);                   %across trial mean
            elseif uv.chooseFluoresenceOrRate == 2                              %if user selected to classify the event rates
                nullDist = nullDistEvtRate;                                     %direct transfer
                empiricalTrialWin = nanmean...
                    (caEvtRateTrials(:,evtWinIdx.(evts{e})),2);                 %within trial average
                empiricalWinAvg = nanmean(empiricalTrialWin);                   %across trial mean
            end
            clear empiricalTrialWin
            %%
            sdNull = nanstd(nullDist(:));                                          %calculate the standard deviation of the null distribution
            upperSD = nanmean(nullDist(:)) + (uv.sigma*sdNull);                    %calculate upper limit of interval around the mean
            lowerSD = nanmean(nullDist(:)) - (uv.sigma*sdNull);                    %calculate lower limit of interval around the mean
            clear sdNull nullDist
            %%
            respClass.(evts{e}).activated(u,1) = empiricalWinAvg > upperSD;     %classify as activated if empirical response exceeds upper limit
            respClass.(evts{e}).inhibited(u,1) = empiricalWinAvg < lowerSD;     %classify as inhibited if empirical response exceeds lower limit
            clear upperSD lowerSD empiricalWinAvg
            %% store trial by trial data
            unitXTrials(u).(evts{e}).caEvtCts = caEvtCtTrials;                  %store evoked calcium event counts over all trials
            unitXTrials(u).(evts{e}).caEvtRate = caEvtRateTrials;               %store evoked calcium event rates over all trials
            unitXTrials(u).(evts{e}).caTraces = caTraceTrials;                  %store evoked calcium traces over all trials
            %% store unit averaged data
            unitAVG.(evts{e}).caEvtCts(u,:) = nanmean(caEvtCtTrials);           %store trial averaged event counts
            unitAVG.(evts{e}).caEvtRates(u,:) = nanmean(caEvtRateTrials);       %store trial averaged event rates
            unitAVG.(evts{e}).caTraces(u,:) = nanmean(caTraceTrials);           %store trial averaged calcium traces
            clear caEvtCtTrials caTraceTrials caEvtRateTrials
        end
        clear u unitTS unitTrace
        %%
    end
    clear e eTS evts numMeasurements
    toc
    
    final(i).name = processed(i).name;
    final(i).mouseID = processed(i).mouseID;
    final(i).treatment = processed(i).treatment;
    final(i).numIcs = processed(i).numIcs;
    final(i).evtWinIdx = evtWinIdx;
    final(i).nullDistEvtRate = nullDistEvtRate;
    final(i).nullDistTrace = nullDistTrace;
    final(i).respClass = respClass;
    final(i).time = time;
    final(i).unitAVG = unitAVG;
    final(i).unitXTrials = unitXTrials;
    final(i).uv = uv;
    
    clear evtWinIdx nullDistEvtRate nullDistTrace respClass time unitAVG unitXTrials unitSD unitAverage
end
clear behav ca i