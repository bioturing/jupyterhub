const path = require('path');
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const { stylePaths } = require("./stylePaths");
const HOST = process.env.HOST || "localhost";
const PORT = process.env.PORT || "9000";
const express = require("express");

module.exports = merge(common('development'), {
  mode: "development",
  devtool: "eval-source-map",
  devServer: {
    contentBase: path.resolve(__dirname, "dist"),
    port: 9000,
    before: (app, server) => {
      const user_data = {
					"last_activity": "2021-10-03T03:42:45.405186Z",
					"created": "2021-09-30T10:24:21.605147Z",
					"server": null,
					"kind": "user",
					"name": "tan@bioturing.com",
					"roles": [
							"user"
					],
					"groups": [],
					"pending": null,
					"admin": false,
					"profile_list": [{"display_name": "Datascience notebook - Small Instance", "slug": "datascience-small", "default": true, "kubespawner_override": {"image": "jupyter/datascience-notebook:2343e33dec46", "cpu_limit": 2, "mem_limit": "4G"}}, {"display_name": "Datascience notebook - Medium Instance", "slug": "datascience-medium", "kubespawner_override": {"image": "jupyter/datascience-notebook:2343e33dec46", "cpu_limit": 4, "mem_limit": "8G"}}, {"display_name": "Datascience notebook - Large Instance", "slug": "datascience-large", "kubespawner_override": {"image": "jupyter/datascience-notebook:2343e33dec46", "cpu_limit": 8, "mem_limit": "16G"}}],
					"servers": {
							"data-science-medium": {
									"name": "data-science-medium",
									"last_activity": "2021-10-03T03:12:26.485000Z",
									"started": "2021-10-03T03:12:14.216294Z",
									"pending": null,
									"ready": true,
									"url": "/jupyterhub/user/tan@bioturing.com/data-science-medium/",
									"user_options": {"profile" : "datascience-small"},
									"progress_url": "/jupyterhub/hub/api/users/tan@bioturing.com/servers/data-science-medium/progress"
							}
					},
					"scopes": [
							"access:servers!user=tan@bioturing.com",
							"read:servers!user=tan@bioturing.com",
							"read:tokens!user=tan@bioturing.com",
							"read:users!user=tan@bioturing.com",
							"read:users:activity!user=tan@bioturing.com",
							"read:users:groups!user=tan@bioturing.com",
							"read:users:name!user=tan@bioturing.com",
							"servers!user=tan@bioturing.com",
							"tokens!user=tan@bioturing.com",
							"users:activity!user=tan@bioturing.com"
					]
			};
      const group_data = JSON.parse(
        '[{"kind":"group","name":"testgroup","users":[]}, {"kind":"group","name":"testgroup2","users":["foo", "bar"]}]'
      );
      const profile_list = [
        {
            "display_name": "Datascience notebook - Small Instance",
            "slug": "datascience-small",
            "default": true,
            "kubespawner_override": {
                "image": "jupyter/datascience-notebook:2343e33dec46",
                "cpu_limit": 2,
                "mem_limit": "4G"
            }
        },
        {
            "display_name": "Datascience notebook - Medium Instance",
            "slug": "datascience-medium",
            "kubespawner_override": {
                "image": "jupyter/datascience-notebook:2343e33dec46",
                "cpu_limit": 4,
                "mem_limit": "8G"
            }
        },
        {
            "display_name": "Datascience notebook - Large Instance",
            "slug": "datascience-large",
            "kubespawner_override": {
                "image": "jupyter/datascience-notebook:2343e33dec46",
                "cpu_limit": 8,
                "mem_limit": "16G"
            }
        }
    ];
    const nb_data = [
      {
          "category": "RNA-Velocity",
          "description": "scVelo is a scalable toolkit for RNA velocity analysis in single cells, based on Bergen et al. (Nature Biotech, 2020)." + 
                         "This is the DentateGyrus notebook that reproduces the analysis from the paper", 
          "display_name": "scVelo - Bergen et al. (Nature Biotech, 2020)",
          "name": "DentateGyrus",
          "filename": "velocyto/DentateGyrus.ipynb",
          "id": 1,
          "format": "IPython",
          "env_filename": "velocyto/environment.yaml",
          "tools": ["scvelo"]
      },	
  ]
		const spawner_progress = {"data": {
			"progress": 100,
			"ready": true,
			"message": "Server ready at /jupyterhub/user/tan@bioturing.com/Tan/",
			"html_message": "Server ready at <a href=\"/jupyterhub/user/tan@bioturing.com/Tan/\">/jupyterhub/user/tan@bioturing.com/Tan/</a>",
			"url": "/jupyterhub/user/tan@bioturing.com/Tan/"
	}};
      app.use(express.json());

      app.get("/nbk/", (req, res) => {
        res.status(200).send(JSON.stringify(nb_data))
      })

      app.get("/hub/home/*", (req, res) => {
        res.status(200).sendFile(path.resolve(__dirname, "dist/index.html"),)
      })
      // get user_data
      app.get("/hub/api/user", (req, res) => {
        res.status(200).set("Content-Type", "application/json")
          .send(JSON.stringify(user_data));
      });
			app.get("/hub/api/users/:username/servers/:servername/progress", (req, res) => {
				const step = Math.round((new Date().getTime() / 1000) % 5);
				spawner_progress.data.progress = step * 20;
				spawner_progress.data.ready = step === 5 ? true : false;
				res.status(200).set("Content-Type", "text/event-stream").send(`data: ${JSON.stringify(spawner_progress)}`);
			});
      // get group_data
      app.get("/hub/api/groups", (req, res) => {
        res
          .set("Content-Type", "application/json")
          .send(JSON.stringify(group_data));
      });
      // add users to group
      app.post("/hub/api/groups/*/users", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
      // remove users from group
      app.delete("/hub/api/groups/*", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
      // add users
      app.post("/hub/api/users", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
			app.post("/hub/spawn/:username/:servername", (req, res) => {
				console.log(req.url, req.body);
        res.status(200).end();
			})
      // delete user
      app.delete("/hub/api/users", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
      // get server profile list
      app.get("/hub/userapi/profile-list", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).send(JSON.stringify(profile_list));
      }) 
      // start user server
      app.post("/hub/api/users/*/server", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
      // stop user server
      app.delete("/hub/api/users/*/server", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
      // shutdown hub
      app.post("/hub/api/shutdown", (req, res) => {
        console.log(req.url, req.body);
        res.status(200).end();
      });
    },
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        include: [
          ...stylePaths
        ],
        use: ["style-loader", "css-loader"]
      }
    ]
  }
});
