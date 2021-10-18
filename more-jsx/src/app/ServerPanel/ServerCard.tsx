import React from 'react';
import {
  Card,
  CardTitle,
  CardBody,
  Gallery,
  Title,
  DescriptionList,
  DescriptionListGroup,
  DescriptionListTerm,
  DescriptionListDescription,
  Flex,
	FlexItem,
  Stack,
  Label
} from '@patternfly/react-core';

import InfoCircleIcon from '@patternfly/react-icons/dist/esm/icons/info-circle-icon';
import { Button } from '@patternfly/react-core'; 
import PropTypes from 'prop-types';


const ServerCard = (props) => {
  const {
    name,
    user_options,
    key,
    ready,
    url,
		profile
  } = props;

  /*
    Jupyterhub parsed submit-form elements as array so
    we have to coercise them into correct type
    */
  const processUserOptions = function(kube_profile) {
    const stringKeys = ["image", "mem_limit"];
    const numericKeys = ["cpu_limit"];
    for (const k in kube_profile) {
      if (k in numericKeys && kube_profile[k] instanceof Array) {
        kube_profile[k] = parseInt(kube_profile[k][0])
      } else if (k in stringKeys && kube_profile[k] instanceof Array) {
        kube_profile[k] = kube_profile[k][0];
      }
    }
    return kube_profile;
  }

  const getReadyStatus = function(isready) {
    if (isready)
      return "green"
    else
      return "orange"
  }

  const kube_profile = processUserOptions("kubespawner_override" in profile ? profile.kubespawner_override : {});
  return (
    <Card isCompact isExpanded key={key}>
        <CardTitle>
          <Flex justifyContent={{ default: 'justifyContentSpaceBetween' }} grow={{ default: 'grow' }}>
						<FlexItem>
							<Title headingLevel="h3" size="xl">
								{name}
							</Title>
						</FlexItem>
            <FlexItem>
							<Button component="a" href={url} target="_blank" isDisabled={!ready} variant="secondary" isSmall>
										Open 
							</Button>{' '}
						</FlexItem>
          </Flex>
          
        </CardTitle>
        <CardBody>
         
          <DescriptionList isCompact>
          <DescriptionListGroup>
              <DescriptionListTerm>Status</DescriptionListTerm>
              <DescriptionListDescription>
                <Label icon={<InfoCircleIcon />} color={getReadyStatus(ready)}>
                  {ready ? "Ready" : "NotReady"} 
                </Label> 
              </DescriptionListDescription>
            </DescriptionListGroup>
            <DescriptionListGroup>
              <DescriptionListTerm>Base image</DescriptionListTerm>
              <DescriptionListDescription>
                 {kube_profile["image"]} 
              </DescriptionListDescription>
            </DescriptionListGroup>
	    <Flex>
        <Flex>
					<Stack>
					<DescriptionListTerm>CPUs</DescriptionListTerm>
						<DescriptionListDescription>
						{kube_profile["cpu_limit"]}
						</DescriptionListDescription>
					</Stack>
				</Flex>
				<Flex>
					<Stack>
						<DescriptionListTerm>RAM</DescriptionListTerm>
						<DescriptionListDescription>
						{kube_profile["mem_limit"]}
						</DescriptionListDescription>
					</Stack>
				</Flex>
	    </Flex> 
			<Flex>
			
			</Flex>
          </DescriptionList>
        </CardBody>
      </Card>
    )
  }

const ServerCardList = (props) => {
  const {
    servers,
		profileList
  } = props;
  return (
    <Gallery hasGutter style={{ '--pf-l-gallery--GridTemplateColumns--min': '260px' }}>
     {servers.map((server, i) => {
       server.key = i;
			 server.profile = {}
			 for (let  i = 0 ; i < profileList.length; i++ ) {
					if (profileList[i].slug === server.user_options.profile) {
						server.profile = profileList[i];
					}
			 }
       return ServerCard(server)
     })} 
    </Gallery>
  );
};

ServerCard.propTypes = {
    name: PropTypes.string,
    ready: PropTypes.bool,
    key: PropTypes.number, 
    user_options :PropTypes.object,
}

ServerCardList.propTypes = {
  servers: PropTypes.arrayOf(PropTypes.exact({
    name: PropTypes.string,
    ready: PropTypes.bool,
    key: PropTypes.number, 
    user_options :PropTypes.object,
		profile: PropTypes.object
  })),
	profileList: PropTypes.array
}

export default ServerCardList;