import React, { useEffect, useState } from 'react';
import { Progress, ProgressVariant } from '@patternfly/react-core';
import { Redirect } from 'react-router';
import { getSpawningProgressURL } from '../../services/server';


import { 
	PageSection, 
	Text,
	TextContent,
  PageSectionVariants,
} from '@patternfly/react-core';

import {normalizeRoute} from '../routes';

const useProgressHook = function(evtSource) {
	const [progressData, setProgressData] = useState({failed: false, ready: false, url:"/#", progress:0, message: "Notebook server is spawning..."});
	useEffect(() => {
		const handleDataChange = function(data) {
			setProgressData(data);
		}
		// hook up event-stream for progress. Adapt to the original jupyterhub codebase
		
		evtSource.onmessage = function(e) {
			let evt = JSON.parse(e.data);
			console.log("evt:", evt);

			handleDataChange(evt);
	
			if (evt.ready) {
				evtSource.close();
				// reload the current page
				// which should result in a redirect to the running server
				window.location.href = evt.url;
			}

			if (evt.failed) {
				evtSource.close();
			}	

		evtSource.onerror = function(err) {
				console.error("EventSource failed:", err);
				setProgressData({failed: true, ready: false, url:"/#", progress:10, message: "Error happend when getting message from server!"});
				evtSource.close();
		};
			
		};
		return;
	}, [])
	
	return progressData;
}
const Spawning = (props) => {	
	
	const {user, serverName} = props.match.params;
	const spawnerProgressUrl = getSpawningProgressURL(user, serverName);
	let evtSource = new EventSource(spawnerProgressUrl);
	const progressData = useProgressHook(evtSource);
	const getVariantProgress = function() {
		if (progressData.ready) {
			return ProgressVariant.success; 
		} else if (progressData.failed) {
			return ProgressVariant.danger; 
		} else {
			return undefined; 
		}
	}
	return (
		<div>
		<PageSection variant={PageSectionVariants.light}>
			<TextContent>
				<Text component="h1">Your new notebook server is starting...</Text>
			</TextContent>
			
		</PageSection>
		<PageSection>
		<Progress value={progressData.progress} title={progressData.message} variant={getVariantProgress()} isTitleTruncated />
		</PageSection>
	</div>
	)
}

export { Spawning };
