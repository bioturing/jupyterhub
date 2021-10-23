import React, { useEffect, useState } from 'react';
import { Progress, ProgressVariant } from '@patternfly/react-core';
import { Redirect } from 'react-router';
import { getSpawningProgressURL, spawnNewserver, spawnNotebook} from '../../services/server';
import {getNotebookPendingEndpoint, getNotebookUrl} from '../../services/utils';

import {
	PageSection,
	Text,
	TextContent,
	PageSectionVariants,
} from '@patternfly/react-core';

const Spawning = (props) => {

	const { user, id} = props.match.params;
	const spawnerProgressUrl = getSpawningProgressURL(user);
	let evtSource = new EventSource(spawnerProgressUrl);
	const [serverReady, setServerReady] = useState(false);
	const [retries, setRetries] = useState(0);
	const [progressData, setProgressData] = useState({ retries: retries, failed: false, ready: false, url: "/#", progress: 0, message: "Notebook server is spawning..." });

	if (!serverReady && retries == 0) {
		spawnNewserver(user);
		setRetries(retries + 1);
	}

	useEffect(() => {
		const handleDataChange = function (data) {
			data.retries = retries
			setProgressData(data);
		}

		// hook up event-stream for progress. Adapt to the original jupyterhub codebase

		evtSource.onmessage = function (e) {
			let evt = JSON.parse(e.data);
			console.log("evt:", evt);

			handleDataChange(evt);

			if (evt.ready) {
				if (!serverReady) {
					setServerReady(true);
				}
				evtSource.close();
				// reload the current page
				// which should result in a redirect to the running server
				// window.location.href = evt.url;
			} else {
				spawnNewserver(user);
			}

			if (evt.failed) {
				if (retries > 0) {
					evtSource.close();
				} else {
					spawnNewserver(user);
					setRetries(retries + 1);
					handleDataChange(evt);
				}
			}

			evtSource.onerror = function (err) {
				console.error("EventSource failed:", err);
				setProgressData({ retries:retries, failed: true, ready: false, url: "/#", progress: 10, message: "Error happend when getting message from server!" });
				evtSource.close();
			};

		};

		

		return;
	}, [])

	const [provisionId, setProvisionId] = useState(null);
	const [nbSpawnError, setNbSpawnError] = useState(false);
	useEffect(() => {
		console.log("inside the spawnNotebook hook, ", serverReady);
		if (serverReady == true) {
			spawnNotebook(user, id)
			.then(res => {
				console.log("Return of provisioning:", res.data);
				setProvisionId(res.data.uuid);
			})
			.catch(err => {
				setNbSpawnError(true);
				console.log("err when spawn the notebook, ", err);
			})
		}
	}, [serverReady])

	const [provisionData, setProvisionData] = useState({
		envname: null, 
		logmess: '',
		notebookname: null,
		progress: 0,
		status: '',
		useremail: null});
	useEffect(() => {
		if (provisionId !== null) {
			const ws = new WebSocket(getNotebookPendingEndpoint(user, provisionId));
			ws.onopen = function() {
				console.log("wss Connected");
				ws.send("Hi this is web client");
			}

			ws.onerror = function(event) {
				console.error("WebSocket error observed:", event);
			};

			ws.onmessage = function(e) {
				const msg = JSON.parse(e.data);
				// TODO: Add type JSON data check sanity here
				setProvisionData(msg);
				if (msg.status == "Success") {
					window.location.href = getNotebookUrl(user, msg.notebookname);	
				}
			}
			ws.onclose = function(e) {
				console.log("wss connection closed");
			}
	}
		
	}, [provisionId])



	const getVariantProvision = function () {
		if (provisionData.status == 'Success') {
			return ProgressVariant.success;
		} else if (provisionData.status == 'Failed' || nbSpawnError) {
			return ProgressVariant.danger;
		} else {
			return undefined;
		}
	}

	const getVariantProgress = function () {
		if (progressData.ready) {
			return ProgressVariant.success;
		} else if (progressData.failed) {
			return ProgressVariant.danger;
		} else {
			return undefined;
		}
	}

	const getSpawningText = function() {
		if (provisionId === null) {
			return  <Text component="h1">Your new notebook server is starting...</Text>;
		} else {
			return <Text component="h1">Provisioning notebook {provisionData.notebookname}...</Text>
		}
	}

	const getSpawningProgresBar = function() {
		if (provisionId === null) {
			return <Progress value={progressData.progress} title={progressData.message} variant={getVariantProgress()} isTitleTruncated />;
		} else {
			return <Progress value={provisionData.progress} title={provisionData.logmess} variant={getVariantProvision()} isTitleTruncated />
		}
		
	}
	return (
		<div>
			<PageSection variant={PageSectionVariants.light}>
				<TextContent>
					{getSpawningText()}
				</TextContent>

			</PageSection>
			<PageSection>
				{getSpawningProgresBar()}
			</PageSection>
		</div>
	)
}

export { Spawning };
